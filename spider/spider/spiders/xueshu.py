import scrapy
import logging
from scrapy.spiders import CrawlSpider
from urllib import parse
from spider.utils import utils
from spider.configs import base_setting
from spider.items import XueShuItem


# from scrapy_redis.spiders import RedisSpider
# class XueShuSpider(RedisSpider):


class XueShuSpider(CrawlSpider):
    name = 'xueshu'

    def __init__(self, name, key_word, max_page, min_page=1, *args, **kwargs):
        self.base_url = "https://s.ixueshu.com/?"
        self.refer = "https://www.ixueshu.com/"
        self.name = name
        config = utils.get_config(name)
        self.config = config
        self.allowed_domains = config.get("allowed_domains")
        self.key_word = key_word
        if max_page > 50:
            max_page = 50
        self.max_page = max_page
        self.min_page = min_page
        self.current_refer = self.refer
        super(XueShuSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        base_setting.IXUESHU_START['q'] = self.key_word
        query_string = parse.urlencode(base_setting.IXUESHU_START)
        start_url = self.base_url + query_string

        self.log("start request url is {}".format(start_url), level=logging.INFO)

        yield scrapy.Request(
            url=start_url,
            headers={"Referer": self.refer},
            callback=self.parse_link_list
        )

    def parse_link_list(self, response):
        # page = response.xpath(
        #     "//div/em[@class='c-3']/following-sibling::text()"
        # ).extract_first()
        # if not page:
        #     max_page = 0
        # else:
        #     page = page.replace("”相关结果", "").replace("条", "")
        #     max_page = (int(page) // 12) + 1

        # 网站默认最多50页(未登录状态下)
        max_page = 50
        self.log("total page is {}".format(max_page), level=logging.INFO)

        for page_num in range(self.min_page, self.max_page + 1):
            if page_num <= int(max_page):
                base_setting.IXUESHU_LINK['q'] = self.key_word
                base_setting.IXUESHU_LINK['page'] = page_num
                query_string = parse.urlencode(base_setting.IXUESHU_LINK)
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
        items = response.xpath("//ul[@class='doc-list active']//li")
        for item in items:
            url = item.xpath(".//div//a[@class='mi']/@href").extract_first()

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
        item = XueShuItem()
        weight = 10
        item['search_word'] = self.key_word
        item['download'] = None
        info = response.xpath("//div/h2/following-sibling::div")
        item['title'] = str(response.xpath("//div//h1/text()").extract_first()).strip()

        authors = info.xpath("//p[contains(text(),'【作者】')]/a/text()").extract()
        length = int(len(authors)/2)
        item['author'] = [author.strip() for author in authors[:length]]
        if len(item['author']) == 0:
            weight -= 3
            item['author'] = None

        key_words = info.xpath(
            ".//p[contains(text(),'【关键词】')]/a/text()"
        ).extract()
        item['keyword'] = ["".join(key_word).strip() for key_word in key_words]
        if len(item['keyword']) == 0:
            weight -= 2
            item['keyword'] = None

        source = info.xpath(
            ".//p[contains(text(),'【刊名】')]/text()"
        ).extract_first()
        item['source'] = source.replace("【刊名】", "")
        if item['source'] is None:
            weight -= 1

        item['doi'] = None
        weight -= 1
        item['type'] = "期刊"
        item['time'] = "".join(
            info.xpath(
                ".//p[contains(text(),'【出版日期】')]/text()"
            ).extract()
        ).strip().replace("【出版日期】", "")

        item['link'] = response.meta['link']
        item['link_md5'] = utils.get_md5(item['link'])

        digest = "".join(info.xpath(".//p[contains(text(),'【摘要】')]/text()").extract()).strip().replace("【摘要】", "摘要：")
        if digest == "":
            weight -= 3
            item['digest'] = None
        else:
            item['digest'] = digest.replace("\n", "").replace("\t", "").replace(" ", "")

        item['weight'] = weight

        self.log("{} was finished".format(response.meta['link']), level=logging.INFO)

        # print(item)
        yield item

