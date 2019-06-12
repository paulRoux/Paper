import os
from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, session, request
from application import db
from werkzeug.utils import secure_filename
from common.libs.utils import check_pwd, generate_password, generate_salt
from common.libs.UrlManager import UrlManager
from common.models.user import User, UserLog
from common.forms.user import LoginForm, RegisterForm, PwdForm, UserInfoForm, UserEditForm

route_user = Blueprint("user_page", __name__)


@route_user.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if "login_user_id" in session:
            flash("账号已登录", category='err')
            return render_template("login.html", form=form)
        data = form.data
        user = User.query.filter_by(name=data['name']).first()
        if user:
            if not check_pwd(user.pwd, data['pwd'], user.salt):
                flash("密码错误", category='err')
                return redirect(UrlManager.build_url_path("user_page.login"))
            session['login_user'] = user.name
            session['login_user_id'] = user.id
            session['quit'] = False
            userlog = UserLog.query.filter_by(user_id=user.id).first()
            if userlog:
                userlog.ip = request.remote_addr
                userlog.login_time = datetime.now()
            else:
                userlog = UserLog(
                    user_id=user.id,
                    ip=request.remote_addr
                )
            db.session.add(userlog)
            db.session.commit()
        else:
            flash("用户名错误", category='err')
            return redirect(UrlManager.build_url_path("user_page.login"))
        if "keyword" in session:
            if session['keyword'] is not None and session['keyword'] != "":
                return redirect(UrlManager.build_url_path("index_page.search"))
        return redirect(UrlManager.build_url_path("index_page.index"))

    return render_template("login.html", form=form)


@route_user.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(
            name=data['name'],
            pwd=generate_password(data['pwd'], generate_salt(len(data['name']))),
            email=data['email'],
        )
        db.session.add(user)
        db.session.commit()
        flash("注册成功", category='ok')
        return redirect(UrlManager.build_url_path("user_page.login"))

    return render_template("register.html", form=form)


@route_user.route('/logout')
def logout():
    session.pop('login_user', None)
    session.pop('login_user_id', None)
    session['quit'] = True
    flash('退出登陆成功', category='ok')
    return redirect(UrlManager.build_url_path("user_page.login"))


@route_user.route("/info", methods=['GET'])
def info():
    if "login_user_id" not in session:
        flash("请先登录", category='err')
        return redirect(UrlManager.build_url_path("user_page.login"))
    login_user = User.query.get_or_404(int(session['login_user_id']))
    form = UserInfoForm(
        name=login_user.name,
        email=login_user.email,
        info=login_user.info
    )

    return render_template("info.html", form=form, login_user=login_user)


@route_user.route("/edit", methods=['GET', 'POST'])
def edit():
    if "login_user_id" not in session:
        flash("请先登录", category='err')
        return redirect(UrlManager.build_url_path("user_page.login"))
    login_user = User.query.get_or_404(int(session['login_user_id']))
    form = UserEditForm(
        name=login_user.name,
        email=login_user.email,
        info=login_user.info
    )
    form.face.validators = []
    form.face.render_kw = {"required": False}
    if form.validate_on_submit():
        data = form.data
        if form.face.data:
            face_save_path = UrlManager.build_image_url("/")
            if not os.path.exists(face_save_path):
                os.makedirs(face_save_path)
                import stat
                os.chmod(face_save_path, stat.S_IRWXU)

            if form.face.data:
                if login_user.face and os.path.exists(os.path.join(face_save_path, login_user.face)):
                    os.remove(os.path.join(face_save_path, login_user.face))
                file_face = secure_filename(form.face.data.filename)
                from common.libs.utils import change_filename
                login_user.face = change_filename(file_face)
                form.face.data.save(face_save_path + login_user.face)

        if login_user.name != data['name'] and User.query.filter_by(name=data['name'].count) == 1:
            flash("账号已存在", category='err')
            return redirect(UrlManager.build_url_path("user_page.edit"))
        login_user.name = data['name']

        if login_user.email != data['email'] and User.query.filter_by(email=data['email']).count() == 1:
            flash("邮箱已存在", category='err')
            return redirect(UrlManager.build_url_path("user_page.edit"))
        login_user.email = data['email']

        login_user.info = data['info']

        db.session.commit()
        flash("修改资料成功", category='ok')
        return redirect(UrlManager.build_url_path("user_page.info"))

    return render_template("edit.html", form=form, login_user=login_user)


@route_user.route("/pwd", methods=['GET', 'POST'])
def reset_pwd():
    login_user = User.query.get_or_404(int(session['login_user_id']))
    form = PwdForm()
    if form.validate_on_submit():
        data = form.data
        if check_pwd(login_user.pwd, data['old_pwd'], login_user.salt):
            new_pwd = generate_password(data['new_pwd'], login_user.salt)
            if login_user.pwd == new_pwd:
                flash('新密码不能和原密码相同', category='err')
                return redirect(UrlManager.build_url_path('user_page.pwd'))
            login_user.pwd = new_pwd
            db.session.commit()
            flash('密码修改成功，请重新登录', category='ok')
            return redirect(UrlManager.build_url_path('user_page.login'))
        else:
            flash('原密码不正确', category='err')
            return redirect(UrlManager.build_url_path("user_page.pwd"))

    return render_template('pwd.html', form=form)

