#### 项目概要

- 论文数据爬取并清洗，存储到MongoDB数据库。通过网页的形式来提供给用户。

#### 爬取内容

1. 爬取来源

    1. 爬取万方、知网、爱学术数据的关键信息，包括：
        - 搜索关键词
        - 标题
        - 作者
        - 关键词
        - 来源
        - 类型
        - doi
        - 文章链接
        - 出版日期
        - 摘要

    3. 其他(TODO)
        - 百度文库
        - 360学术
        - 其他的论文网站(优先)

2. 使用

    - 本项目基于：`python3.6` `redis` `mysql5.7` `mongodb`
    
    - 下载本仓库的代码，在根目录下执行 `pip install -r requirements.txt` 安装相关的环境
        - 然后进入根目录的 `mysql_init.py` 中修改自己的 `MySQL` 要连接的数据库的 `URI` (提前在MySQL里面建好数据库) 以及 `SECRET_KEY` 加密字符串
        - 修改完了之后在根目录下执行 `python mysql_init.py` 来初始化数据库
    
    - 然后根目录执行 `python manager.py runserver` 来运行项目
    
    - 接下来在网页中输入你要访问的服务器地址和端口(默认`127.0.0.1:5000`)，IP可以自己设置
    
    - 最后在前端页面搜索框输入自己想要搜索的论文的关键词即可
        - 如果数据库里面是空的，会在后台自己爬取相关数据(默认爬取两页(按时间))，然后自动的在前端页面展示，所以要多等待几秒
        - 本项目设置了用户的相关模块，不登录默认只显示一页，用户可以先注册，然后登陆查询即可

3. 其他
    - 本项目默认开启`日志`记录功能，级别为`INFO`
        - 爬虫的日志在爬虫根目录下的`spider/spider/`下的`crawler.log`文件里面
        - 前端的日志在项目根目录下的下的`flask.log`文件里面

    - 本项目默认不开启代理池，如果要开启的话，在爬虫根目录下的`spider/spider/settings.py`里面找到`DOWNLOADER_MIDDLEWARES`把注释去掉
        - 然后在项目根目录的`configs/setting.py`里面将`IPPROXY`改为`True`
    
    - 本项目默认不开启`redis`存储，如果要开启的话，在`spider/spider/spiders/`下面将除过`__init__.py`的文件的`class`以及上面的头文件的注释去掉
        - 然后在`spider/spider/settings.py`里面将最后的关于`redis`的注释去掉(栈和队列只需要一个即可)
        - 接着找到`spider/spider/configs/`下面除过`base_setting.py`的`json`文件，在`ITEM_PIPELINES`里面加上`"scrapy_redis.pipelines.RedisPipeline": 460`，并注释掉上面一句关于`MongoDB`的配置
    
    - 本项目默认不开启`cnkiwap`的爬取，如果需要开启，取消在项目根目录下的`configs/setting.py`里面的`DATABASE`和`COLLECTION`中关于`cnikwap`的注释
    
    - 本项目默认爬取数据的页数为`1页`，如果需要调整，修改在项目根目录下的`configs/setting.py`里面的`MAX_PAGE`，最大值为100页
    
    - 本项目还存在一些没有发现的问题，和许多功能的完善及增加