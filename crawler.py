from time import sleep

import requests

from abc import ABC, abstractmethod

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

from config import BASE_URL, HEADER, CITY

from threading import Thread
from queue import Queue

from storage import MongoStorage

from parse import Parser


class BaseCrawl(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def store(self, data):
        pass

    @staticmethod
    def get(url, header=None):
        try:
            response = requests.get(url, headers=header)
        except requests.HTTPError:
            print('unable to get response and there is no status code')
            return None
        return response


class LinkCrawl(BaseCrawl):
    def __init__(self):
        self.base_url = BASE_URL
        self.city = CITY
        self.mongodb = MongoStorage('adv_links')

    def select_city(self):
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
        url = self.select_city() + "&page={}"
        queue = Queue()
        for i in range(1, 21):
            queue.put(url.format(i))
        return queue

    def crawl(self, queue):
        while queue.qsize():
            url = queue.get()
            links = self.get_links(self.get(url, header=HEADER).text)
            links_dicts = [{"link": lnk, "flag": False} for lnk in links]
            self.store(links_dicts)
            queue.task_done()

    def start(self):
        threads = list()
        queue = self.create_queue()
        for _ in range(6):
            thread = Thread(target=self.crawl, args=(queue,))
            threads.append(thread)
            thread.start()
        for t in threads:
            t.join()

    def store(self, data):
        self.mongodb.store(data)


class DataCrawl(BaseCrawl):
    def __init__(self):
        self.mongodb_load = MongoStorage("dav_links")
        self.mongodb_store = MongoStorage("adv_data")
        self.parser = Parser()
        self.links = self.mongodb_load.load({'flag': False})

    def create_queue(self):
        queue = Queue()
        for link in self.links:
            queue.put(link)
        return queue

    def crawl(self, queue):
        while queue.qsize():
            link = queue.get()
            html = self.get(link["url"], header=HEADER).text
            self.store(self.parser.parse_all_data(html))
            self.mongodb_store.update_flag(link)
            queue.task_done()

    def start(self):
        threads = list()
        queue = self.create_queue()
        for _ in range(7):
            thread = Thread(target=self.crawl, args=(queue,))
            threads.append(thread)
            thread.start()
        for t in threads:
            t.join()

    def store(self, data):
        self.mongodb_store.store(data)
