# -*- coding: utf-8 -*-

from models import User

def validate_username(username):
    if User.query.filter_by(username=username).first():
        return False
    else:
        return True