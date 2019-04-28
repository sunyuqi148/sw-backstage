# -*- coding: utf-8 -*-
from flask import json
from flask_login import UserMixin

from ext import db

import datetime

## These classes should inherit flask.ext.login.UserMixin.
## See: https://flask-login.readthedocs.io/en/latest/
##      or 
##      https://www.cnblogs.com/agmcs/p/4445428.html


class Validity:
    # args: valid
    def __init__(self, valid = False,
                     info = ''):
        self._valid = valid
        self._info = info
    
    # rets: a json string of validity
    def get_resp(self):
        return json.dumps({'valid': self._valid,' info': self._info})
#        return Response(json.dumps({'valid': self._valid,
#                                    'info': self._info}),
#                        content_type='application/json')


# Membership of some user for some group
membership = db.Table('membership',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)


# Friendship between user and user
friendship = db.Table('friendship',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('friend_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)


# All users
class User(UserMixin, db.Model):
    # id, username, password, name, info, tasks, friends
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(24), nullable=False,
                         unique=True)
    password = db.Column(db.String(24), nullable=False)
    name = db.Column(db.String(24), nullable=False)
    info = db.Column(db.String(1024)) 
    tasks = db.relationship('Task', backref='user', lazy='dynamic')
    friends = db.relationship('User', #defining the relationship, User is left side entity
                                secondary = friendship, 
                                primaryjoin = (friendship.c.user_id == id), 
                                secondaryjoin = (friendship.c.friend_id == id),
                                lazy = 'subquery'
                            )
    
    def __init__(self, username, password,
                 name=None,
                 info=''
                 ):
        self.username = username
        self.password = password
        if name is None:
            self.name = self.username
        else:
            self.name = name
        self.info = info
        
    def get_id(self):
        return self.id
    
    # rets: json map includes valid=true and user_id
    def get_resp(self):
        pass
    
    def get_friendlist_resp(self):
        pass
    
    # rets: a json string of all tasks belonging to user
    def get_tasklist_resp(self):
        pass
    
    # rets: a json string of all tasks belonging to user's friends
    def get_friend_tasklist_resp(self):
        pass
    
    # rets: a json string of all tasks belonging to groups the user belongs to
    def get_group_tasklist_resp(self):
        pass
    
    def update(self, 
               username=None,
               password=None,
               name=None,
               info=None
               ):
        if username is not None and User.query.filter_by(username=username).first():
            self.username = username
        if password is not None:
            self.password = password
        if name is not None:
            self.name = name
        if info is not None:
            self.info = info
            
    # rets: False if friend_id is already a friend of user
    #       True, else
    def add_friend(user_id, friend_id):
        pass
            
    # rets: False if user does not have this friend
    #       True, else
    def delete_friend(user_id, friend_id):
        pass


# All groups
class Group(db.Model):
    # id, name, owner_id, info, tasks, members
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    info = db.Column(db.String(1024))
    tasks = db.relationship('Task',
                            backref='group',
                            lazy='dynamic'
                            )
    members = db.relationship('User',
                              secondary=membership,
                              lazy='subquery',
                              backref=db.backref('groups', lazy=True)
                              )
    
    def __init__(self, name, owner_id, info=''):
        self.name = name
        self.owner_id = owner_id
        self.info = info
        
    def get_id(self):
        return self.id
    
    # rets: json map includes valid=true and user_id
    def get_resp(self):
        pass
    
    # rets: a json string of all tasks belonging to group
    def get_tasklist_resp(self):
        pass
    
    def update(self, 
               name=None,
               owner_id=None,
               info=None
               ):
        if name is not None:
            self.name = name
        if owner_id is not None and User.query.filter_by(id=owner_id).first():
            self.owner_id = owner_id
        if info is not None:
            self.info = info
            
    # rets: False if friend_id is already a friend of user
    #       True, else
    def add_member(self, user_id):
        pass
        
    # rets: False if user does not have this friend
    #       True, else
    def delete_member(self, user_id):
        pass


# All tasks (DDLs)
class Task(db.Model):
    # id, owner_id, title, create_time, finish_time, status, group, info
    # status: 0-ongoning, 1-finished, 2-due
    # publicity: 0-private, 1-public, 2-group task
    # If group task, group_id is not none
    __tablename__ = 'task'
    __id = db.Column(db.Integer, primary_key=True)
    __owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    __title = db.Column(db.String(1024), nullable=False)
    __create_time = db.Column(db.DateTime, nullable=False)
    __finish_time = db.Column(db.DateTime, nullable=False)
    __status = db.Column(db.Integer, nullable=False)
    __publicity = db.Column(db.Integer, nullable=False)
    __group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    __info = db.Column(db.String(1024))
    
    def __init__(self, owner_id, title, finish_time,
                 status=0,
                 publicity=0,
                 group_id=None,
                 info=''
                 ):
        self.__owner_id = owner_id
        self.__title = title
        self.__create_time = datetime.datetime.now()
        self.__finish_time = finish_time
        self.__status = status
        self.__publicity = publicity
        if self.__publicity == 2:
            self.__group_id = group_id
        else:
            self.__group_id = None
        self.__info = info
        
    def get_id(self):
        return self.id
    
    # rets: a map includes valid=true and user_id
    def get_info_map(self):
        return {'title': self.__title,
                'create_time': self.__create_time,
                'finish_time': self.__finish_time,
                'status': self.__status,
                'publicity': self.__publicity,
                'info': self.__info}
    
    def update(self, 
               owner_id=None,
               title=None,
               finish_time=None,
               status=None,
               publicity=None,
               group_id=None,
               info=None
               ):
        if owner_id is not None and User.query.filter_by(id=owner_id).first():
            self.__owner_id = owner_id
        if title is not None:
            self.__title = title
        if finish_time is not None:
            self.__finish_time = finish_time
        if status is not None:
            self.__status = status
        if publicity is not None:
            self.__publicity = publicity
        if self.__publicity == 2 and group_id is not None:
            self.__group_id = group_id
        if info is not None:
            self.__info = info
