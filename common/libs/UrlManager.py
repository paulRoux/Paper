from time import time
from application import app
from flask import url_for
from configs.setting import APPLICATION


class UrlManager(object):
    def __init__(self):
        pass

    @staticmethod
    def build_url(path):
        return path

    @staticmethod
    def build_path(path):
        return APPLICATION['domain'] + path

    @staticmethod
    def build_url_path(path):
        return url_for(path)

    @staticmethod
    def build_url_name(path, name):
        if name == "":
            return UrlManager.build_url_path(path)
        return url_for(path, name=name)

    @staticmethod
    def build_static_url(path):
        release_version = app.config.get('RELEASE_VERSION')
        ver = "{}".format(int(time())) if not release_version else release_version
        path = "/static" + path + "?ver=" + ver
        return UrlManager.build_url(path)

    @staticmethod
    def build_image_url(path):
        app_config = app.config['APPLICATION']
        url = app_config['domain'] + app.config['UPLOAD']['prefix_url'] + path
        return url
