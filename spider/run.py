import argparse
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spider.utils import utils, check_db


def run():
    """ 输入参数列表：name, keyword, maxpage mongo_uri, mongo_db 可选 """

    arg_settings = {}
    parser = argparse.ArgumentParser()
    parser.add_argument("name", type=str, help="input the spider name")
    parser.add_argument("-k", "--keyword", help="input the keyword of the spider to search")
    parser.add_argument("-m", "--maxpage", help="input the maxpage of the start_urls page")
    parser.add_argument(
        "-u",
        "--mongouri",
        help="input the uri of mongodb like: mongodb://<username>:<password>@hostname:port or mongodb://hostname:port"
    )
    parser.add_argument("-d", "--dbname", help="input the name of mongodb")
    args = parser.parse_args()
    name = args.name
    if args.keyword:
        arg_settings["KEY_WORD"] = args.keyword
    if args.maxpage:
        arg_settings["MAX_PAGE"] = int(args.maxpage)
    if args.mongouri:
        arg_settings["MONGO_URI"] = args.mongouri
    if args.mongouri:
        arg_settings["MONGO_DB"] = args.dbname

    custom_settings = utils.get_config(name)
    spider = custom_settings.get('spider')
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    settings.update(custom_settings.get('settings'))
    settings.update(arg_settings)
    key_word = settings.get('KEY_WORD')
    max_page = settings.get('MAX_PAGE')
    # if CheckDb(name, key_word).check_db():
    #     # TODO 前端获取数据
    #     return
    process = CrawlerProcess(settings)
    process.crawl(spider, **{'name': name, 'key_word': key_word, 'max_page': max_page})
    process.start()


if __name__ == "__main__":
    run()
