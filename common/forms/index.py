from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class IndexForm(FlaskForm):
    keyword = StringField(
        label="关键字:",
        description="关键字",
        render_kw={
            "class": "from-control",
            "style": "border-radius: 30px; width: 260px; height: 45px",
        }
    )

    submit = SubmitField(
        label="搜索一下",
        render_kw={
            "class": "ui circular teal basic compact button",
        }
    )



