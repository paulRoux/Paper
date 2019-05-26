# -*- coding: utf-8 -*-
import scrapy
import logging
from urllib import parse
from spider.utils import utils
from spider.configs import base_setting
from spider.items import CnkiWapItem

# from scrapy_redis.spiders import RedisSpider
# class CnkiWapSpider(RedisSpider):


class CnkiWapSpider(scrapy.Spider):
    name = 'cnkiwap'

    def __init__(self, name, key_word, max_page, min_page=1, *args, **kwargs):
        config = utils.get_config(name=name)
        self.list_url = "http://wap.cnki.net/touch/web/Article/Search"
        self.current_referer = "http://wap.cnki.net/touch/web"
        self.config = utils.get_config(name=self.name)
        self.page_size = 10
        self.key_word = key_word
        self.min_page = min_page
        self.max_page = max_page
        self.allowed_domains = config.get("allowed_domains")
        super(CnkiWapSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        base_setting.CNKI_WAP_START['kw'] = self.key_word
        query_string = parse.urlencode(base_setting.CNKI_WAP_START)
        start_url = self.list_url + '?' + query_string

        self.log("start request url is {}".format(start_url), level=logging.INFO)

        yield scrapy.Request(
            url=start_url,
            headers={"Referer": self.current_referer},
            cookies={'cookiejar': 1},
            callback=self.parse_request
        )

    def parse_request(self, response):
        self.current_referer = response.request.url
        base_setting.CNKI_WAP_PARSE['pagesize'] = str(self.page_size)
        base_setting.CNKI_WAP_PARSE['keyword'] = self.key_word

        self.log("prepare request {}".format(self.list_url), level=logging.INFO)

        yield scrapy.FormRequest(
            url=self.list_url,
            headers={"Referer": self.current_referer},
            method='POST',
            meta={'cookiejar': 1},
            formdata=base_setting.CNKI_WAP_PARSE,
            callback=self.parse_link_list,
            dont_filter=True
        )

    def parse_link_list(self, response):
        page_size = response.xpath('//span[@id="totalcount"]/text()').extract_first()
        if not page_size:
            max_page = 0
        else:
            max_page = int(page_size) // 10 + 1

        self.log("total page_size is {}".format(str(page_size)), level=logging.INFO)
        self.log("total page is {}".format(str(max_page)), level=logging.INFO)

        for page_num in range(self.min_page, self.max_page + 1):
            if page_num <= max_page:
                base_setting.CNKI_WAP_PARSE['pageindex'] = str(page_num)

                self.log("prepare crawl the {} page!".format(self.list_url), level=logging.INFO)

                yield scrapy.FormRequest(
                    url=self.list_url,
                    headers={"Referer": self.current_referer},
                    method='POST',
                    meta={'cookiejar': page_num + 1, 'page': page_num},
                    formdata=base_setting.CNKI_WAP_PARSE,
                    callback=self.parse_link,
                    dont_filter=True
                )
            else:
                break
            # break

    def parse_link(self, response):
        link_list = response.xpath('//a[@class="c-company-top-link"]/@href').extract()

        for links in link_list:
            if "http" not in links:
                url = "http:" + links
            else:
                url = links

            self.log("prepare to crawl: {}".format(url), level=logging.INFO)

            yield scrapy.Request(
                url=url,
                meta={'cookiejar': response.meta['cookiejar']},
                headers={"Referer": self.current_referer},
                callback=self.parse_item
            )
            # break

    def parse_item(self, response):
        item = CnkiWapItem()
        weight = 10
        item['search_word'] = self.key_word

        item['title'] = str(response.xpath(
            "//div[@class='c-card__title2']/text()"
        ).extract_first()).strip()

        authors = response.xpath(
            "//div[@class='c-card__author']//a[@class='author-icon']/following-sibling::a/text()"
        ).extract()
        item['author'] = [author.strip() for author in authors]
        if len(item['author']) == 0:
            weight -= 3
            item['author'] = None

        keywords = response.xpath(
            "//div[contains(text(),'关键词')]/following-sibling::*/a/text()"
        ).extract()
        item['keyword'] = [key.strip() for key in keywords]
        if len(item['keyword']) == 0:
            weight -= 2
            item['keyword'] = None

        sources = response.xpath("//div[@class='c-card__paper-content']//a/text()").extract()
        item['source'] = [source.strip().replace(";", "") for source in sources]
        if item['source'] is None:
            weight -= 1

        # item['region'] = response.xpath(
        #     "//div[contains(text(),'领　域')]/following-sibling::*/a/text()"
        # ).extract_first()

        item['doi'] = None
        weight -= 1
        item['time'] = None
        item['type'] = "期刊"
        item['link'] = response.request.url
        item['link_md5'] = utils.get_md5(item['link'])

        digest = "".join(response.xpath("//div[@class='c-card__aritcle']/text()").extract()).strip()
        if digest == "":
            weight -= 3
            item['digest'] = None
        else:
            item['digest'] = digest.replace("\n", "").replace("\t", "").replace(" ", "")

        item['weight'] = weight

        self.log("{} was finished".format(response.request.url), level=logging.INFO)

        # print(item)
        yield item
