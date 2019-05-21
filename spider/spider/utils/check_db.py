from pymongo import MongoClient
from spider.configs.base_setting import MONGODB


class CheckDb(object):
    def __init__(self, name, search_word):
        self.mongo_uri = MONGODB['uri']
        self.mongo_db = MONGODB['db']
        self.search_word = search_word
        self.name = name

    def open_mongo(self):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def check_db(self):
        self.open_mongo()
        table = self.name.capitalize() + "Item" + MONGODB['collection']
        if self.db[table].find_one({"search_word": "search_word"}):
            self.close_mongo()
            return True
        else:
            self.close_mongo()
            return False

    def close_mongo(self):
        self.client.close()
