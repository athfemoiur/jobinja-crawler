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
        #  flag is used for not crawling a link more than one time
        self.collection.update_one({'_id': link['_id']}, {'$set': {'flag': True}})


class MysqlStorage:
    @staticmethod
    def store(links):
        """
        :param links: links is a list of dictionaries
        """
        for link in links:
            Link.get_or_create(url=link["link"])

    @staticmethod
    def store_data(link, data):
        """
        :param data: data is a python dict
        :param link: link is a peewee model object
        """
        company = Company.get_or_create(name=data["Company name"], description=data["Company description"])
        company = company[0]
        adv = Advertisement.create(link=link, title=data["Title"], description=data["Description"], company=company,
                                   remaining_days=data["Remaining days"])

        for key, value in list(data.items())[5:]:
            if isinstance(value, list):
                value = ",".join(value)
            Tag.create(key=key, value=value, advertisement=adv)

    @staticmethod
    def load_links():
        return Link.select().where(Link.flag == False)

    @staticmethod
    def update_flag(link):
        link.flag = True
        link.save()
