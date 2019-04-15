# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 19:57:39 2019

@author: 38192
"""

from flask import (Flask, request)
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

SECRET_KEY = 'This is my key'

app = Flask(__name__)
db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(24), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@127.0.0.1/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)


@app.route("/")
def hello():
    user = User("sample_user", "psw")
    db.session.add(user)
    db.session.commit()
    user = User.query.filter_by(username='sample_user').first()
    if user:
        print(user.username)
        print(user.password)
    return "Hello World!"
    
#    return "Hello World!"
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
