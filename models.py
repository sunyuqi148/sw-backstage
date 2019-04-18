# -*- coding: utf-8 -*-
from flask import json
from flask_login import UserMixin

from ext import db
import time

## These classes should inherit flask.ext.login.UserMixin.
## See: https://flask-login.readthedocs.io/en/latest/
##      or 
##      https://www.cnblogs.com/agmcs/p/4445428.html

class User(UserMixin, db.Model):
    # args: username, password
    # rets: user_id (if valid)
    #		False (if invalid)
    
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False)
    password = db.Column(db.String(24), nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def get_id(self):
        return self.id
	
#	# args: user_id
#    def get(user_id):
#        pass # TODO: implement this function

	# rets: user_id (if valid)
	#       False (if invalid)
#    def register_user(username, password):
#        pass

	# rets: json map includes valid=true and user_id
    def get_resp():
        pass
		
    def get_friendlist_resp():
        pass
		
	# rets: user_id of friend, if the username exists
	#       False, if username is invalid
    def get_friend_id(username):
        pass
		
	# rets: False if friend_id is already a friend of user
	#       True, else
    def add_friend(user_id, friend_id):
        pass
		
	# rets: False if user does not have this friend
	#       True, else
    def delete_friend(user_id, friend_id):
        pass
				

class Task(db.Model):
	# title, deadline, desciption, task_id, user_id(maybe)
    __tablename__ = 'todolist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(1024), nullable=False)
    status = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.Integer, nullable=False)

    def __init__(self, user_id, title, status):
        self.user_id = user_id
        self.title = title
        self.status = status
        self.create_time = time.time()
	
#    def __init__(user_id, title, deadline, description):
#        pass
	
	# rets: a json string of all tasks belonging to user
    def get_todolist_resp(user_id):
        pass
						
	# Generates response including task id, valid = True
    def get_resp():
        pass
		
	# returns NULL if task_id is invalid.
    def get_task(user_id, task_id):
        pass
		
    def delete_task(user_id, task_id):
        pass
	
    def finish_task(user_id, task_id):
        pass
	
    def modify_title():
        pass
	
    def modify_deadline():
        pass
	
    def modify_description():
        pass


class Validity:
	# args: valid
    def __init__(self, valid = False,
                     info = ''):
        self._valid = valid
        self._info = info
	
	# rets: a json string of validity
    def get_resp(self):
        return Response(json.dumps({'valid': self._valid,
									'info': self._info}),
						content_type='application/json')