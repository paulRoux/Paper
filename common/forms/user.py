from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from common.models.user import User
from common.libs.utils import check_pwd


class LoginForm(FlaskForm):
    name = StringField(
        label="账号:",
        validators=[
            DataRequired("请输入账号")
        ],
        description="账号",
        render_kw={
            "class": "from-control",
            "style": "border-radius: 30px; width: 260px",
            "required": "required"
        }
    )

    pwd = PasswordField(
        label="密码:",
        validators=[
            DataRequired("请输入密码")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "style": "border-radius: 30px; width: 260px"
        }
    )

    submit = SubmitField(
        label="登陆",
        render_kw={
            "class": "ui small circular blue basic button"
        }
    )

    register = SubmitField(
        label="注册",
        render_kw={
            "class": "ui small circular blue basic button"
        }
    )

    def validate_account(self, field):
        account = field.data
        count = User.query.filter_by(name=account).count()
        if count == 0:
            raise ValidationError("账号不存在")


class RegisterForm(FlaskForm):
    name = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！")
        ],
        description="账号",
        render_kw={
            "class": "form-control input-lg",
            "style": "border-radius: 30px; width: 260px"
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱！"),
            Email("邮箱格式不正确")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control input-lg",
            "style": "border-radius: 30px; width: 260px"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control input-lg",
            "style": "border-radius: 30px; width: 260px"
        }
    )
    repwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入重复密码！"),
            EqualTo("pwd", message="两次密码不一致")
        ],
        description="密码",
        render_kw={
            "class": "form-control input-lg",
            "style": "border-radius: 30px; width: 260px"
        }
    )
    info = TextAreaField(
        label="简介",
        description="简介",
        render_kw={
            "class": "form-control input-lg",
            "style": "border-radius: 30px; width: 260px",
            "rows": "5"
        }
    )
    submit = SubmitField(
        label="提交",
        render_kw={
            "class": "ui small circular blue basic button"
        }
    )

    def validate_name(self, field):
        name = field.data
        num = User.query.filter_by(name=name).count()
        if num == 1:
            raise ValidationError("账号已经存在，请重新输入")

    def validate_email(self, field):
        email = field.data
        num = User.query.filter_by(email=email).count()
        if num == 1:
            raise ValidationError("邮箱已经存在，请重新输入")


class PwdForm(FlaskForm):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码！")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "style": "border-radius: 30px; width: 260px"
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码！")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "style": "border-radius: 30px; width: 260px"
        }
    )

    repwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入重复密码！"),
            EqualTo("new_pwd", message="两次密码不一致")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "style": "border-radius: 30px; width: 260px"
        }
    )

    submit = SubmitField(
        label="提交",
        render_kw={
            "class": "ui small circular blue basic button"
        }
    )

    def validate_old_pwd(self, field):
        """检查验证旧密码是否正确"""
        from flask import session
        old_pwd = field.data
        login_name = session["login_user"]
        admin = User.query.filter_by(name=login_name).first()
        if not check_pwd(admin.pwd, old_pwd, admin.salt):
            raise ValidationError("原密码错误！")


class UserInfoForm(FlaskForm):
    name = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "style": "border-radius: 30px; width: 260px",
            "readonly": True
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱！"),
            Email("邮箱格式不正确")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control",
            "style": "border-radius: 30px; width: 260px",
            "readonly": True
        }
    )
    face = FileField(
        label='头像',
        validators=[
            DataRequired('请上传头像')
        ],
        description='头像',
    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介！")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "style": "border-radius: 30px; width: 260px",
            "rows": "5",
            "readonly": True
        }
    )
    submit = SubmitField(
        label="保存",
        render_kw={
            "class": "ui small circular blue basic button"
        }
    )


class UserEditForm(FlaskForm):
    name = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "style": "border-radius: 30px; width: 260px",
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱！"),
            Email("邮箱格式不正确")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control",
            "style": "border-radius: 30px; width: 260px",
        }
    )
    face = FileField(
        label='头像',
        validators=[
            DataRequired('请上传头像')
        ],
        description='头像',
    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介！")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "style": "border-radius: 30px; width: 260px",
            "rows": "5",
        }
    )
    submit = SubmitField(
        label="保存",
        render_kw={
            "class": "ui small circular blue basic button"
        }
    )
