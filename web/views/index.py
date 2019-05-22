import pymongo
import math
from multiprocessing import Pool
from application import db, app
from flask import render_template, Blueprint, session, flash, redirect, request
from common.forms.index import IndexForm
from common.models.user import UserLog
from common.libs.segmentation import Segmentation
from common.libs.utils import run_spider, get_max_length
from common.libs.UrlManager import UrlManager
from configs.setting import DATABASE, URI, COLLECTION, SEARCH_DB, SEARCH_COL, APPLICATION, PAGE_SIZE

route_index = Blueprint("index_page", __name__)


@route_index.route("/", methods=['GET', 'POST'])
def index():
    form = IndexForm()
    data = {
        "keyword": None,
        "url": ""
    }
    session['show'] = False
    session['word'] = None

    if form.validate_on_submit():
        session['keyword'] = form.data['keyword']
        data['keyword'] = session['keyword']

        if session['keyword'] is not None and session['keyword'] != "":
            if len(session['keyword']) < 2:
                flash("输入的关键词太短", 'err')
                return redirect(UrlManager.build_url_path("index_page.find"))
            if "login_user_id" in session:
                userlog = UserLog.query.filter_by(user_id=session['login_user_id'])
                session['show'] = True
                userlog.search_word = session['keyword']
                db.session.commit()
            url = UrlManager.build_url_path("index_page.search") + "?search_word=" + data['keyword']
            data['url'] = APPLICATION['domain'] + url
            session['word'] = session['keyword']
            session['keyword'] = None
            return redirect(data['url'])

    return render_template("index.html", form=form, data=data)


@route_index.route("/search", methods=['GET', 'POST'])
def search():
    page = request.args.get("p", "")  # 页数
    show_home = False  # 显示首页状态
    if page == "":
        page = 1
    else:
        page = int(page)
        if page > 1:
            show_home = True
    page_size = PAGE_SIZE  # 起始
    session['find'] = False

    keyword = None
    if "keyword" in session and session['keyword'] is not None:
        if len(session['keyword']) > 1:
            keyword = session['keyword']
        else:
            flash("输入的关键词太短", 'err')
            return redirect(UrlManager.build_url_path("index_page.find"))
    else:
        keyword = request.values.get("search_word")

    if keyword is not None:
        keyword = keyword.strip()
    else:
        flash("请输入关键词搜索", 'err')
        return redirect(UrlManager.build_url_path("index_page.find"))
    session['word'] = keyword
    url = APPLICATION['domain'] + "/search?search_word=" + keyword
    data = {
        "keyword": keyword,
        "is_page": False,
        "show_home": show_home,
        "total": 0,
        "page": int(page),
        # "dic_list": "",
        "url": url,
        "is_login": False,
        "results": []
    }

    number = 0  # 分页使用
    client = pymongo.MongoClient(URI)
    db = client[SEARCH_DB]
    collection = db[SEARCH_COL]
    # word = collection.find_one({"keyword": data['keyword']})
    seg_list = []
    seg = Segmentation()
    seg.set_sentence(keyword)
    seg.rmm_seg()
    segment = seg.get_result_dict()
    max_len = get_max_length(segment)
    for value in segment.values():
        for val in value:
            if len(val) >= max_len:
                seg_list.append(val)

    word = []
    words = collection.find()
    for value in words:
        for s in seg_list:
            if s == value['keyword'] or value['keyword'] in s:
                word.append(s)
            elif s in value['keyword']:
                word.append(value['keyword'])

    if not word:
        if data['keyword'] is not None and data['keyword'] != "":
            session['find'] = True
            pool = Pool()
            count = 0
            result_list = []
            for base in DATABASE.values():
                result = pool.apply_async(run_spider, (base, data['keyword']))
                result_list.append(result)

            pool.close()
            pool.join()
            for re in result_list:
                if re.get() is False:
                    count += 1
                    app.logger.info("crawler has an error")
                if count >= len(DATABASE):
                    session['find'] = False
                    data['is_page'] = False
                    flash("暂时没有找到数据", "err")
                    return redirect(UrlManager.build_url_path("index_page.find"))
            data['is_page'] = True
            app.logger.info("crawler was successful")
            return redirect(UrlManager.build_url_path("index_page.find"))
        else:
            data = None
    else:
        res_list = []
        for value in DATABASE.values():
            db = client[value]
            for val in COLLECTION.values():
                if val == value + "Item":
                    collection = db[val]
                    if len(word) != 1:
                        for key in word:
                            res = collection.find({"search_word": key}).sort(
                                [('weight', pymongo.DESCENDING), ('_id', pymongo.DESCENDING)]
                            ).limit(page_size).skip(
                                page_size * page
                            )
                            if res is not None or res != "":
                                res_list.append(res)
                                number += res.count()
                    else:
                        res = collection.find({"search_word": data['keyword']}).sort(
                            [('weight', pymongo.DESCENDING), ('_id', pymongo.DESCENDING)]
                        ).limit(page_size).skip(
                            page_size * page
                        )
                        if res is not None or res != "":
                            res_list.append(res)
                            number += res.count()
                    if len(res_list) != 0:
                        data['is_page'] = True
                        data['results'].append(res_list)
                    else:
                        flash("没有找到数据", "err")
                        data['is_page'] = False
                        session['find'] = False
                        return redirect(UrlManager.build_url_path("index_page.find"))
                else:
                    continue
        total = int((math.ceil(number / page_size) / len(DATABASE)))  # 总页数
        if "login_user_id" in session:
            data['total'] = total
            data['is_login'] = True
        else:
            data['total'] = 1
        # dic = get_page(total, page)
        # data['dic_list'] = dic
    client.close()

    return render_template("search.html", data=data)


@route_index.route("/find")
def find():
    data = {
        "keyword": session['word']
    }
    if session['find']:
        session['keyword'] = data['keyword']
        # flash("查找数据完成，请点击上面搜索按钮继续搜索!", "ok")
        return redirect(UrlManager.build_url_path("index_page.search"))
    return render_template("find.html", data=data)
