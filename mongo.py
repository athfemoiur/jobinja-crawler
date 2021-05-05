from pymongo import MongoClient


class MongoDataBase:
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        self.__client = MongoClient()
        self.database = self.__client["jobinja"]
