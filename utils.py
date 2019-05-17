# -*- coding: utf-8 -*-
import datetime

from models import User, Group, Task

# Validating methods
def validate_userid(user_id):
    if User.query.filter_by(id=user_id).first():
        return True
    else:
        return False


# when new add a user, check whether there is a same username
def validate_username(username):
    if User.query.filter_by(username=username).first():
        return False
    else:
        return True


def validate_groupid(group_id):
    if Group.query.filter_by(id=group_id).first():
        return True
    else:
        return False


def validate_taskid(task_id):
    if Task.query.filter_by(id=task_id).first():
        return True
    else:
        return False


def validate_friendship(user_id, friend_id):
    if validate_userid(user_id):
        user = User.query.filter_by(id=user_id).first()
        friend_ids = [friend.id for friend in user.get_friends()]
        if friend_id in friend_ids:
            return True
        else:
            return False
    else:
        return False


# Ownership if a group
def validate_ownership(user_id, group_id):
    if Group.query.filter_by(id = group_id, owner_id = user_id).first():
        return True
    else:
        return False


def validate_membership(user_id, group_id):
    group = Group.query.filter_by(id=group_id).first()
    member_ids = [member.id for member in group.get_members()]
    if group is not None and user_id in member_ids:
        return True
    else:
        return False


# Ownership of a task
def validate_task_ownership(user_id, task_id):
    if Task.query.filter_by(id=task_id, owner_id=user_id).first():
        return True
    else:
        return False
    
def trans_to_date(str_time):
    str_time = str_time.split()
    d = str_time[0].split('-')
    t = str_time[-1].split(':')
    time = datetime.datetime(int(d[0]), int(d[1]), int(d[2]),
                             int(t[0]), int(t[1]), int(t[2]))
    return time
