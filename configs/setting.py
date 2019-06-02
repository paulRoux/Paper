SERVER_PORT = 5000
DEBUG = True

SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1/Paper?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ENCODING = "utf8mb4"

SECRET_KEY = 'roux'

# 版本号
RELEASE_VERSION = "0.2"

APPLICATION = {
    'domain': 'http://127.0.0.1:5000'
}

# 上传配置
UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/static/upload/'
}

URI = "mongodb://localhost:27017"

# 关键词数据库配置
SEARCH_DB = "search_word"
SEARCH_COL = "words"

# 数据库
DATABASE = {
    "cnki": "Cnki",
    "wanfang": "WanFang",
    "ixueshu": "XueShu",
    # "cnkiwap": "CnkiWap"
}

# 数据库表
COLLECTION = {
    "cnki": "CnkiItem",
    "wanfang": "WanFangItem",
    "ixueshu": "XueShuItem",
    # "cnkiwap": "CnkiWapItem"
}

# 每页显示的条数
SIZE = 6

# 根据数据库的多少来设置正个页面的显示量
PAGE_SIZE = SIZE // len(DATABASE)

# 是否设置 IP 代理
IP_PROXY = "False"

# 爬取的最大页数
MAX_PAGE = 1
