import scrapy
import logging
from scrapy.spiders import CrawlSpider
from urllib import parse
from spider.utils import utils
from spider.configs import base_setting
from spider.items import WanFangItem

# from scrapy_redis.spiders import RedisSpider
# class WanfangSpider(RedisSpider):


class WanfangSpider(CrawlSpider):
    name = 'wanfang'

    def __init__(self, name, key_word, max_page, min_page=1, *args, **kwargs):
        self.base_url = "http://wanfangdata.com.cn/search/searchList.do?"
        self.item_url = "http://www.wanfangdata.com.cn/details/detail.do?"
        self.refer = "http://www.wanfangdata.com.cn/index.html"
        self.name = name
        config = utils.get_config(name)
        self.config = config
        self.allowed_domains = config.get("allowed_domains")
        self.key_word = key_word
        self.max_page = max_page
        self.min_page = min_page
        self.current_refer = self.refer
        super(WanfangSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        base_setting.WANFANG['searchWord'] = self.key_word
        query_string = parse.urlencode(base_setting.WANFANG)
        start_url = self.base_url + query_string

        self.log("start request url is {}".format(start_url), level=logging.INFO)

        yield scrapy.Request(
            url=start_url,
            headers={"Referer": self.refer},
            callback=self.parse_link_list
        )

    def parse_link_list(self, response):
        max_page = response.xpath(
            "//div//ul[@class='clear']//li//span[@class='searchPageWrap_all']/text()"
        ).extract_first()
        if not max_page:
            max_page = 0
        self.log("total page is {}".format(max_page), level=logging.INFO)

        for page_num in range(self.min_page, self.max_page + 1):
            if page_num <= int(max_page):
                base_setting.WANFANG_NEXT['page'] = page_num
                base_setting.WANFANG_NEXT['searchWord'] = self.key_word
                query_string = parse.urlencode(base_setting.WANFANG_NEXT)
                url = self.base_url + query_string

                self.log("prepare crawl the {} page!".format(page_num), level=logging.INFO)

                yield scrapy.Request(
                    url=url,
                    headers={"Referer": self.current_refer},
                    callback=self.parse_link
                )
                self.current_refer = url
            else:
                break
            # break

    def parse_link(self, response):
        self.current_refer = response.request.url
        items = response.xpath("//div[@class='ResultBlock']//div")
        for item in items:
            doctype = item.xpath(".//div[@class='ResultCheck']/input[@name='selectBox']/@doctype").extract_first()
            docid = item.xpath(".//div[@class='ResultCheck']/input[@name='selectBox']/@docid").extract_first()
            if docid is None or doctype is None:
                continue
            base_setting.WANFANG_ITEM['_type'] = doctype
            base_setting.WANFANG_ITEM['id'] = docid
            query_string = parse.urlencode(base_setting.WANFANG_ITEM)
            url = self.item_url + query_string

            self.log("prepare to crawl: {}".format(url), level=logging.INFO)

            yield scrapy.Request(
                url=url,
                headers={"Referer": self.current_refer},
                dont_filter=True,
                meta={"link": url},
                callback=self.parse_item
            )
            # break

    def parse_item(self, response):
        item = WanFangItem()
        weight = 10
        item['search_word'] = self.key_word
        info = response.xpath("//div[@class='left_con_top']")
        item['title'] = str(info.xpath(".//div[@class='title']/text()").extract_first()).strip()

        # authors = info.xpath(
        #     ".//div[contains(text(),'作者：')]/following-sibling::div//a[contains(@id, 'card')]/text()"
        # ).extract()
        authors = info.xpath(
            "//div[contains(text(), '作者：')]/following-sibling::div/input/@value"
        ).extract()
        # item['author'] = [author.strip() for author in authors]
        for value in authors:
            if value == "":
                authors.remove(value)
        authors.reverse()
        print(authors)
        item['author'] = [author.strip() for author in authors[1::2]]
        if len(item['author']) == 0:
            weight -= 3
            item['author'] = None

        key_words = info.xpath(
            ".//ul[@class='info']//div[contains(text(),'关键词：')]/following-sibling::div//a/text()"
        ).extract()
        item['keyword'] = ["".join(key_word).strip() for key_word in key_words]
        if len(item['keyword']) == 0:
            weight -= 2
            item['keyword'] = None

        item['source'] = info.xpath(
            ".//ul[@class='info']//div[contains(text(),'刊名：')]/following-sibling::div//a/text()"
        ).extract_first()
        if item['source'] is None:
            weight -= 1

        doi = info.xpath(
            ".//ul[@class='info']//div[contains(text(),'doi：')]/following-sibling::div//a/text()"
        ).extract_first()
        if doi is None or doi == "":
            weight -= 1
            item['doi'] = None
        else:
            item['doi'] = doi

        item['type'] = "期刊"
        item['time'] = "".join(
            info.xpath(
                ".//ul[@class='info']//div[contains(text(),'在线出版日期：')]/following-sibling::div/text()"
            ).extract()
        ).strip()

        item['link'] = response.meta['link']
        item['link_md5'] = utils.get_md5(item['link'])

        digest = "".join(info.xpath(".//div[@class='abstract']//div/text()").extract()).strip()
        if digest == "":
            weight -= 3
            item['digest'] = None
        else:
            item['digest'] = "摘要：" + digest.replace("\n", "").replace("\t", "").replace(" ", "")

        item['weight'] = weight

        self.log("{} was finished".format(response.meta['link']), level=logging.INFO)

        # print(item)
        yield item
