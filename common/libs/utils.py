import random
import hashlib
import base64
import string
import os
import uuid
import subprocess
# from flask import request
from datetime import datetime
from application import app, db
from flask import flash, redirect
from common.libs.UrlManager import UrlManager
from common.models.user import UserLog


# 获取格式化的时间
def get_format_date(date=None, format="%Y-%m-%d %H:%M:%S"):
    if date is None:
        date = datetime.now()
    return date.strftime(format)


def generate_auth_code(user_info=None):
    m = hashlib.md5()
    user_str = "%s-%s-%s-%s" % (user_info.id, user_info.name, user_info.pwd, user_info.salt)
    m.update(user_str.encode("utf-8"))
    return m.hexdigest()


def generate_password(pwd, salt):
    m = hashlib.md5()
    pwd_str = "%s-%s" % (base64.encodebytes(pwd.encode("utf-8")), salt)
    m.update(pwd_str.encode("utf-8"))
    return m.hexdigest()


def generate_salt(length=16):
    key_list = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
    return "".join(key_list)


def check_pwd(pwd, old_pwd, slat):
    return pwd == generate_password(old_pwd, slat)


def check_keyword(keyword):
    if len(keyword) < 2:
        flash("输入的关键词太短", category='err')
        return redirect(UrlManager.build_url_path("index_page.find"))


def check_login_status(session):
    check_keyword(session['keyword'])
    if "login_user_id" in session:
        userlog = UserLog.query.filter_by(user_id=session['login_user_id']).first()
        if userlog:
            userlog.search_word = session['keyword']
            db.session.add(userlog)
            db.session.commit()
        else:
            flash("登录失效,请重新登陆", category='err')
            session.pop('login_user', None)
            session.pop('login_user_id', None)
            return redirect(UrlManager.build_url_path("user_page.login"))
    else:
        flash("登录失效,请重新登陆", category='err')
        if "login_user" in session:
            session.pop('login_user', None)
        return redirect(UrlManager.build_url_path("user_page.login"))


def change_filename(filename):
    fileinfo = os.path.splitext(filename)  # 分离包含路径的文件名与包含点号的扩展名
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex + fileinfo[-1])
    app.logger.info('函数中修改后的文件名：', filename)
    return filename


def run_spider(base, keyword, ip_proxy, max_page):
    if max_page > 100:
        max_page = 100
    cmd = 'python run.py {} -k "{}" -p {} -m {}'.format(base, keyword, ip_proxy, max_page)
    # cwd = os.path.abspath(os.path.join(os.getcwd(), "../../spider"))
    os.getcwd()
    cwd = os.getcwd() + "/spider"
    if os.path.exists(cwd):
        os.chdir(cwd)
        app.logger.info("change dir to {}".format(cwd))
    else:
        app.logger.info("error at change dir to {}".format(cwd))
        return False
    p = subprocess.Popen(cmd, shell=True)
    p.wait()
    if p.returncode != 0:
        app.logger.info("run_spider error")
        return False
    else:
        app.logger.info("run_spider finished")
        return True


# 分页中间的变化
# def get_page(total, p):
#     show_page = 3  # 显示的页码数
#     page_offset = 2  # 偏移量
#     start = 1  # 分页条开始
#     end = total  # 分页条结束
#
#     if total > show_page:
#         if p > page_offset:
#             start = p - page_offset
#             if total > p + page_offset:
#                 end = p + page_offset
#             else:
#                 end = total
#         else:
#             start = 1
#             if total > show_page:
#                 end = show_page
#             else:
#                 end = total
#         if p + page_offset > total:
#             start = start - (p + page_offset - end)
#
#     用于模版中循环
#     dic = range(start, end + 1)
#     return dic


def get_max_length(str_list):
    max_length = 1
    for value in str_list.values():
        for val in value:
            if len(val) > max_length:
                max_length = len(val)
    return max_length


def get_second_length(str_list):
    li = []
    for value in str_list.values():
        for val in value:
            li.append(len(val))
    li.sort(reverse=True)
    return li[1]
