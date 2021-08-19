from time import sleep
import requests
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from config import BASE_URL, HEADER, CITY, DATA_BASE
from threading import Thread
from queue import Queue
from storage import MongoStorage, MysqlStorage
from parse import Parser


class BaseCrawl(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def crawl(self):
        pass

    @staticmethod
    def get(url, header=None, proxy=None):
        try:
            response = requests.get(url, headers=header, proxies=proxy)
        except requests.HTTPError:
            print('unable to get response and there is no status code')
            return None
        print(response.status_code)
        return response


class LinkCrawl(BaseCrawl):
    def __init__(self):
        self.base_url = BASE_URL
        self.city = CITY
        self.storage = MongoStorage('adv_links') if DATA_BASE == 'mongo' else MysqlStorage
        self.queue = self.create_queue()

    def get_city_url(self):
        #  this method uses selenium for selecting the city and return the url
        #  you can change the city from config.py file

        chrome_options = Options()
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.get(self.base_url)
        sleep(0.5)
        selects = driver.find_elements_by_class_name('select2able')
        select = Select(selects[0])
        select.select_by_visible_text(self.city)
        select = Select(selects[1])
        select.select_by_index(1)
        submit = driver.find_element_by_xpath('//*[@id="home2"]/div/div[2]/div[1]/div[2]/div/form/div/div[2]/button')
        submit.click()
        return driver.current_url

    @staticmethod
    def get_links(html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')
        return [lnk.get('href') for lnk in soup.find_all('a', attrs={'class': 'c-jobListView__titleLink'})]

    def create_queue(self):
        url = self.get_city_url() + "&page={}"
        queue = Queue()
        for i in range(1, 21):
            queue.put(url.format(i))
        return queue

    def crawl(self):
        while True:
            #  using python queue and multithreading
            url = self.queue.get()
            links = self.get_links(self.get(url, header=HEADER).text)
            links_dicts = [{"link": lnk, "flag": False} for lnk in links]
            self.store(links_dicts)
            self.queue.task_done()
            if self.queue.empty():
                break

    def start(self):
        #  multithreading
        for _ in range(6):
            thread = Thread(target=self.crawl)
            thread.start()
        self.queue.join()

    def store(self, data):
        self.storage.store(data)


class BaseDataCrawl(BaseCrawl, ABC):
    def __init__(self):
        self.links = None
        self.queue = None
        self.parser = Parser()

    def create_queue(self):
        queue = Queue()
        for link in self.links:
            queue.put(link)
        return queue

    def start(self):
        for _ in range(10):
            thread = Thread(target=self.crawl)
            thread.start()
        self.queue.join()


class MongoDataCrawl(BaseDataCrawl):
    def __init__(self):
        super().__init__()
        self.mongodb_load = MongoStorage('adv_links')
        self.links = self.mongodb_load.load({'flag': False})
        self.mongodb_store = MongoStorage("adv_data")
        self.queue = self.create_queue()

    def crawl(self):
        while True:
            link = self.queue.get()
            url = link["link"]
            response = self.get(url, header=HEADER)
            if response.status_code == 200:
                data = {**{"Advertisement Link": url}, **self.parser.parse_all_data(response.text)}
                self.store(data)
                self.mongodb_load.update_flag(link)
            self.queue.task_done()
            if self.queue.empty():
                break

    def store(self, data):
        self.mongodb_store.store(data)


class MysqlDataCrawler(BaseDataCrawl):

    def __init__(self):
        super().__init__()
        self.storage = MysqlStorage()
        self.links = self.storage.load_links()
        self.queue = self.create_queue()

    def crawl(self):
        while True:
            link = self.queue.get()
            url = link.url
            response = self.get(url, header=HEADER)
            data = self.parser.parse_all_data(response.text)
            if response.status_code == 200:
                self.storage.store_data(link, data)
                self.storage.update_flag(link)
            self.queue.task_done()
            if self.queue.empty():
                break
