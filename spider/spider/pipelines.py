# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import pymongo
from scrapy.exceptions import DropItem
from spider.configs.base_setting import MONGODB


class SpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class CnkiPipeline(object):
    def process_item(self, item, spider):
        if len(item['title']) == "" or item['keyword'] == 0 and len(item['author']) == 0:
            logging.log(msg="the {} item will be dropped".format(item['link']), level=logging.INFO)
            raise DropItem("useless item")
        return item


class CnkiWapPipeline(object):
    def process_item(self, item, spider):
        if len(item['title']) == "" or item['keyword'] == 0 and len(item['author']) == 0:
            logging.log(msg="the {} item will be dropped".format(item['link']), level=logging.INFO)
            raise DropItem("useless item")
        return item


class WanfangPipeline(object):
    def process_item(self, item, spider):
        if len(item['title']) == "" or item['keyword'] == 0 and len(item['author']) == 0:
            logging.log(msg="the {} item will be dropped".format(item['link']), level=logging.INFO)
            raise DropItem("useless item")
        return item


class XueShuPipeline(object):
    def process_item(self, item, spider):
        if len(item['title']) == "" or item['keyword'] == 0 and len(item['author']) == 0:
            logging.log(msg="the {} item will be dropped".format(item['link']), level=logging.INFO)
            raise DropItem("useless item")
        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.name = ""
        self.search_word = ""

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.name = item.__class__.__name__
        if self.db[self.name].find_one({"link_md5": item['link_md5']}):
            self.db[self.name].update_one({"link": item['link']}, {'$set': dict(item)})
        else:
            self.db[self.name].insert(dict(item))
        self.search_word = item['search_word']
        logging.log(msg="save to database of {} was finished".format(self.name), level=logging.INFO)
        return item

    def close_spider(self, spider):
        self.client.close()


class SaveSearchWordPipeline(object):
    def __init__(self):
        self.mongo_uri = MONGODB["uri"]
        self.mongo_db = MONGODB["db"]
        self.search_word = ""
        self.name = ""

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):
        self.search_word = item['search_word']
        data = {
            "keyword": self.search_word,
            "source": [],
            "count": 1,
        }
        self.name = item.__class__.__name__
        # table = self.name + MONGODB['collection']
        table = MONGODB['collection']
        res = self.db[table].find_one({"keyword": self.search_word})
        data['source'].append(self.name)
        if not res:
            self.db[table].insert(dict(data))
        else:
            self.db[table].update_one({"keyword": self.search_word}, {'$inc': {"count": 1}})

        logging.log(msg="save {} searchWord was finished".format(self.name), level=logging.INFO)

        return item

    def close_spider(self, spider):
        self.client.close()
