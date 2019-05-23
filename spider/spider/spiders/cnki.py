# -*- coding: utf-8 -*-
import scrapy
import logging
import time
from urllib import parse
from scrapy.http.cookies import CookieJar
from spider.utils import utils
from spider.configs import base_setting
from spider.items import CnkiItem


# from scrapy_redis.spiders import RedisSpider
# class CnkiSpider(RedisSpider):


class CnkiSpider(scrapy.Spider):
    name = 'cnki'

    def __init__(self, name, key_word, max_page, min_page=1, *args, **kwargs):
        config = utils.get_config(name=name)
        self.base_url = base_setting.CNKI_URL.get("base_url")
        self.home_url = base_setting.CNKI_URL.get("home_url")
        self.list_url = base_setting.CNKI_URL.get("list_url")
        self.current_referer = base_setting.CNKI_URL.get("current_referer")
        self.config = utils.get_config(name=self.name)
        self.key_word = key_word
        self.min_page = min_page
        self.max_page = max_page
        self.allowed_domains = config.get("allowed_domains")
        super(CnkiSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        base_setting.CNKI_START['txt_1_value1'] = self.key_word
        base_setting.CNKI_START["__"] = time.strftime("%a %b %d %Y %H:%M:%S") + " GMT+0800 (中国标准时间)"
        query_string = parse.urlencode(base_setting.CNKI_START)
        start_url = self.home_url + query_string

        self.log("start request url is {}".format(start_url), level=logging.INFO)

        yield scrapy.Request(
            url=start_url,
            headers={"Referer": self.current_referer},
            cookies={CookieJar: self.min_page},
            dont_filter=True,
            callback=self.parse_request
        )

    def parse_request(self, response):
        base_setting.CNKI_PARSE['keyValue'] = self.key_word
        base_setting.CNKI_PARSE['t'] = int(time.time())
        query_string = parse.urlencode(base_setting.CNKI_PARSE)
        url = self.list_url + query_string

        self.log("prepare request {}".format(url), level=logging.INFO)

        yield scrapy.Request(
            url=url,
            headers={"Referer": self.current_referer},
            callback=self.parse_link_list
        )

    def parse_link_list(self, response):
        self.current_referer = response.request.url
        max_page = response.xpath('//span[@class="countPageMark"]/text()').extract_first()
        if not max_page:
            max_page = 0
        else:
            max_page = int(max_page.split("/")[1])

        self.log("total page is {}".format(str(max_page)), level=logging.INFO)

        for page_num in range(self.min_page, self.max_page + 1):
            if page_num <= max_page:
                base_setting.CNKI_PARSE_LIST['curpage'] = page_num
                query_string = parse.urlencode(base_setting.CNKI_PARSE_LIST)
                url = self.list_url + "?" + query_string

                self.log("prepare crawl the {} page!".format(page_num), level=logging.INFO)

                yield scrapy.Request(
                    url=url,
                    headers={"Referer": self.current_referer},
                    callback=self.parse_link
                )
                self.current_referer = url
            else:
                break
            # break

    def parse_link(self, response):
        refer = response.request.url
        link_list = response.xpath("//tr[@bgcolor='#ffffff']|//tr[@bgcolor='#f6f7fb']")
        for links in link_list:
            paper_link = links.xpath(".//td/a[@class='fz14']/@href").extract_first()
            publish_time = "".join(links.xpath(".//td[5]/text()").extract()).strip()
            paper_type = links.xpath(".//td[6]/text()").extract_first().strip()
            year = int(publish_time[0:4])
            url = self.base_url + paper_link
            if 2010 < year <= 2019:
                self.log("prepare to crawl: {}".format(url), level=logging.INFO)
                yield scrapy.Request(
                    url=url,
                    headers={"Referer": refer},
                    meta={
                        "enable_redirect": True,
                        "dont_redirect": False,
                        "cnkiitem": {
                            "publish_time": publish_time,
                            "type": paper_type
                        }
                    },
                    callback=self.parse_item
                )
            # break

    def parse_item(self, response):
        item = CnkiItem()
        weight = 10
        item['search_word'] = self.key_word
        item['title'] = response.xpath(
            "//div[@id='mainArea']//div[@class='wxTitle']/h2[@class='title']/text()"
        ).extract_first()

        authors = response.xpath(
            "//div[@id='mainArea']//div[@class='wxTitle']//div[@class='author']//span/a/text()"
        ).extract()
        item['author'] = [author.strip() for author in authors]
        if len(item['author']) == 0:
            weight -= 1
            item['author'] = None

        keywords = response.xpath("//*[@id='catalog_KEYWORD']/following-sibling::*/text()").extract()
        item['keyword'] = [key.strip().replace(";", "") for key in keywords]
        if len(item['keyword']) == 0:
            weight -= 1
            item['keyword'] = None

        item['source'] = response.xpath(
            "//div[@id='mainArea']//div[@class='wxsour']//div//p[@class='title']/a/text()"
        ).extract_first()
        if item['source'] is None:
            weight -= 1

        doi = response.xpath("//p//*[@id='catalog_ZCDOI']/../text()").extract_first()
        if doi is None or doi == "":
            weight -= 1
            item['doi'] = None
        else:
            item['doi'] = doi

        item['type'] = response.meta['cnkiitem']['type']
        item['time'] = response.meta['cnkiitem']['publish_time']
        item['link'] = response.request.url
        item['link_md5'] = utils.get_md5(item['link'])

        digest = "".join(response.xpath("//*[@id='ChDivSummary']/text()").extract()).strip()
        if digest == "":
            weight -= 2
            item['digest'] = None
        else:
            item['digest'] = "摘要：" + digest.replace("\n", "").replace("\t", "").replace(" ", "")

        item['weight'] = weight

        self.log("{} was finished".format(response.request.url), level=logging.INFO)

        # print(item)
        yield item
