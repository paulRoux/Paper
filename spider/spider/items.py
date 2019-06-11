# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CnkiItem(scrapy.Item):
    search_word = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()
    time = scrapy.Field()
    type = scrapy.Field()
    keyword = scrapy.Field()
    doi = scrapy.Field()
    link = scrapy.Field()
    digest = scrapy.Field()
    link_md5 = scrapy.Field()
    weight = scrapy.Field()
    download = scrapy.Field()


class CnkiWapItem(scrapy.Item):
    search_word = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()
    time = scrapy.Field()
    type = scrapy.Field()
    keyword = scrapy.Field()
    doi = scrapy.Field()
    link = scrapy.Field()
    digest = scrapy.Field()
    link_md5 = scrapy.Field()
    weight = scrapy.Field()
    download = scrapy.Field()


class WanFangItem(scrapy.Item):
    search_word = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()
    time = scrapy.Field()
    type = scrapy.Field()
    keyword = scrapy.Field()
    doi = scrapy.Field()
    link = scrapy.Field()
    digest = scrapy.Field()
    link_md5 = scrapy.Field()
    weight = scrapy.Field()
    download = scrapy.Field()


class XueShuItem(scrapy.Item):
    search_word = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    source = scrapy.Field()
    time = scrapy.Field()
    type = scrapy.Field()
    keyword = scrapy.Field()
    doi = scrapy.Field()
    link = scrapy.Field()
    digest = scrapy.Field()
    link_md5 = scrapy.Field()
    weight = scrapy.Field()
    download = scrapy.Field()
