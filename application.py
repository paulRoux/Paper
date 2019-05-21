# -*- coding: utf-8 -*-
from flask import Flask, render_template
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
import os


class Application(Flask):
    def __init__(self, import_name, template_folder=None, root_path=None):
        super(Application, self).__init__(
            import_name,
            template_folder=template_folder,
            root_path=root_path,
            static_folder=None
        )

        # 配置信息
        self.config.from_pyfile('configs/setting.py')

        db.init_app(self)


db = SQLAlchemy()
app = Application(__name__, template_folder=os.getcwd() + "/web/templates/", root_path=os.getcwd())
manager = Manager(app)


'''
函数模板
'''
from common.libs.UrlManager import UrlManager
app.add_template_global(UrlManager.build_static_url, 'buildStaticUrl')
app.add_template_global(UrlManager.build_url, 'buildUrl')
app.add_template_global(UrlManager.build_image_url, 'buildImageUrl')
app.add_template_global(UrlManager.build_url_path, 'buildUrlPath')
app.add_template_global(UrlManager.build_url_name, 'buildUrlName')
app.add_template_global(UrlManager.build_path, 'buildPath')


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404
