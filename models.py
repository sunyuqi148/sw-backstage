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
    # if True, create with return information
    def __init__(self, valid = False,
                 ret = None):
#                 ret_map = {}):
        if valid:
            self.__map = ret if ret != None else {}
        else: 
            self.__map = {}
            self.__map['error_info'] = ret
        self.__map['valid'] = valid
   
    # rets: a json string of validity
    def get_resp(self):
        return json.dumps(self.__map)
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
    __name = db.Column(db.String(24), nullable=False)
    __info = db.Column(db.String(1024)) 
    __tasks = db.relationship('Task', backref='owner', lazy='subquery')
    __friends = db.relationship('User', #defining the relationship, User is left side entity
                                secondary = friendship, 
                                primaryjoin = (friendship.c.user_id == id), 
                                secondaryjoin = (friendship.c.friend_id == id),
                                lazy = 'subquery'
                                )
    __ownership = db.relationship('Group',
                                  backref='owner',
                                  lazy='subquery'
                                  )
    
    def __init__(self, username, password,
                 name=None,
                 info=''
                 ):
        self.username = username
        self.password = password
        if name is None:
            self.__name = self.username
        else:
            self.__name = name
        self.__info = info
        
    def get_id(self):
        return self.id
    
    # rets: json map includes valid=true and user_id
    def get_resp(self):
        pass
    
    def get_friends(self):
        return self.__friends
    
    def get_groups(self):
        return self.groups
        
    def get_ownership(self):
        return self.__ownership

    # rets: a json string of all tasks belonging to user
    def get_tasks(self):
        return self.__tasks
    
    # rets: a json string of public tasks belonging to user
    def get_public_tasks(self):
        ret = [task for task in self.__tasks if task.get_publicity() == 0]
        return ret
    
    def update(self, 
               username=None,
               password=None,
               name=None,
               info=None
               ):
        if username is not None and not User.query.filter_by(username=username).first():
            self.username = username
        if password is not None:
            self.password = password
        if name is not None:
            self.__name = name
        if info is not None:
            self.__info = info

    def add_friend(self, friend_id):
        friend = User.query.filter_by(id=friend_id).first()
        self.__friends.append(friend)

    def delete_friend(self, friend_id):
        friend = User.query.filter_by(id=friend_id).first()
        if friend in self.__friends:
            self.__friends.remove(friend)


# All groups
class Group(db.Model):
    # id, name, owner_id, info, tasks, members
    __tablename__ = 'group'
    id = db.Column(db.Integer, primary_key=True)
    __name = db.Column(db.String(24), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    __info = db.Column(db.String(1024))
    __tasks = db.relationship('Task',
                              backref='group',
                              lazy='subquery'
                              )
    __members = db.relationship('User',
                                secondary=membership,
                                lazy='subquery',
                                backref=db.backref('groups', lazy=True)
                                )
    
    def __init__(self, name, owner_id, info=''):
        self.__name = name
        self.owner_id = owner_id
        self.__info = info
        user = User.query.filter_by(id=owner_id).first()
        self.__members.append(user)
        
    def get_id(self):
        return self.id
    
    def add_member(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        self.__members.append(user)
        
    def delete_member(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        if user in self.__members:
            self.__members.remove(user)
    
    def get_members(self):
        return self.__members
    
#    def add_task(self, task_id):
#        task = Task.query.filter_by(id=task_id).first()
#        self.__tasks.append(task)
#        
#    def delete_task(self, task_id):
#        pass #TODO
    
    def get_tasks(self):
        return self.__tasks

    def update(self, 
               name=None,
               owner_id=None,
               info=None
               ):
        if name is not None:
            self.__name = name
        if owner_id is not None and User.query.filter_by(id=owner_id).first():
            self.owner_id = owner_id
        if info is not None:
            self.__info = info
            
    def get_info_map(self):
        return {'group_id': self.id,
                'name': self.__name,
                'owner_id':self.owner_id,
                'info': self.__info}


# All tasks (DDLs)
class Task(db.Model):
    # id, owner_id, title, create_time, finish_time, status, group, info
    # status: 0-ongoing, 1-finished, 2-due
    # publicity: 0-private, 1-public, 2-group task
    # If group task, group_id is not none
    __tablename__ = 'task'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
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
        self.owner_id = owner_id
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
    
    def get_publicity(self):
        return self.__publicity
    
    # rets: a map includes valid=true and user_id
    def get_info_map(self):
        return {'task_id': self.id,
                'title': self.__title,
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
            self.owner_id = owner_id
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
