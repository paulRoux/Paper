import random
import hashlib
import base64
import string
import os
import uuid
import subprocess
# from flask import request
from datetime import datetime
from application import app
from configs.setting import MAX_PAGE


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


def change_filename(filename):
    fileinfo = os.path.splitext(filename)  # 分离包含路径的文件名与包含点号的扩展名
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex + fileinfo[-1])
    app.logger.info('函数中修改后的文件名：', filename)
    return filename


def run_spider(base, keyword):
    cmd = 'python run.py {} -m {} -k "{}"'.format(base, MAX_PAGE, keyword)
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
