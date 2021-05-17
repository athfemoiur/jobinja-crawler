from mongo import MongoDataBase

from mysql.models import Link, Advertisement, Company, Tag


class MongoStorage:
    def __init__(self, collection_name):
        self.collection = getattr(MongoDataBase().database, collection_name)

    def store(self, data):
        if isinstance(data, list) and len(data) > 1:
            self.collection.insert_many(data)
        else:
            self.collection.insert_one(data)

    def load(self, filter_query=None):
        if filter_query is not None:
            data = self.collection.find(filter_query)
        else:
            data = self.collection.find()

        return data

    def update_flag(self, link):
        self.collection.update_one({'_id': link['_id']}, {'$set': {'flag': True}})


class MysqlStorage:
    @staticmethod
    def store_link(links):
        """
        :param links: links is a list of dictionaries
        """
        for link in links:
            Link.create(url=link["link"], flag=False)

    @staticmethod
    def store_data(link, data):
        """
        :param data: data is a python dict
        :param link: link is a peewee object
        """
        company = Company.get_or_create(name=data["نام شرکت"], description=data["معرفی شرکت"])
        adv = Advertisement.create(link=link, title=data["عنوان"], description=data["موقعیت شغلی"], company=company[0],
                                   remaining_days=data["فرصت ارسال رزومه"])

    @staticmethod
    def load_links():
        return Link.select().where(Link.flag == 0)
