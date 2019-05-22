SERVER_PORT = 5000
DEBUG = True

SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@127.0.0.1/Paper?charset=utf8mb4'
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_ENCODING = "utf8mb4"

SECRET_KEY = 'roux'

RELEASE_VERSION = "0.1"

APPLICATION = {
    'domain': 'http://127.0.0.1:5000'
}

UPLOAD = {
    'ext': ['jpg', 'gif', 'bmp', 'jpeg', 'png'],
    'prefix_path': '/web/static/upload/',
    'prefix_url': '/static/upload/'
}

URI = "mongodb://localhost:27017"

SEARCH_DB = "search_word"
SEARCH_COL = "words"

DATABASE = {
    "cnki": "Cnki",
    "wanfang": "WanFang",
    # "cnkiwap": "CnkiWap"
}

COLLECTION = {
    "cnki": "CnkiItem",
    "wanfang": "WanFangItem",
    # "cnkiwap": "CnkiWapItem"
}

SIZE = 6

# 根据数据库的多少来设置正个页面的显示量
PAGE_SIZE = SIZE // len(DATABASE)
