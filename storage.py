from mongo import MongoDataBase


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
        self.collection.update_one({'_id': link['id']}, {'$set': {'flag': True}})
