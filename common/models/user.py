from application import db
from datetime import datetime


# from common.libs.utils import generate_password, generate_salt
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
#
# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:123456@127.0.0.1/Paper?charset=utf8mb4'
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
# app.config["SQLALCHEMY_ENCODING"] = "utf8mb4"
# app.config["SQLALCHEMY_ECHO"] = True
# app.config["SECRET_KEY"] = 'roux'
# db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False, unique=True)
    pwd = db.Column(db.String(32), nullable=False)
    salt = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True)
    face = db.Column(db.String(255))
    reg_time = db.Column(db.DateTime, index=True, default=datetime.now())
    info = db.Column(db.Text)
    userlogs = db.relationship('UserLog', backref='user')

    def __repr__(self):
        return "<User {}>".format(self.name)


class UserLog(db.Model):
    __tablename__ = 'userlogs'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ip = db.Column(db.String(64))
    login_time = db.Column(db.DateTime, index=True, default=datetime.now())
    search_word = db.Column(db.String(255))

    def __repr__(self):
        return "<UserLog {}>".format(self.id)


if __name__ == "__main__":
    # db.drop_all()
    # db.create_all()
    #
    # user = User(
    #     name="roux",
    #     pwd=generate_password("roux", generate_salt(len("roux"))),
    #     salt=generate_salt(len("roux")),
    #     email="roux@gmail.com",
    #     info="i am roux"
    # )
    # db.session.add(user)
    # db.session.commit()

    pass
