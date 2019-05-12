# -*- coding: utf-8 -*-
from models import User, Group, Task

# Validating methods
def validate_userid(user_id):
    if User.query.filter_by(id=user_id).first():
        return True
    else:
        return False


# when new add a user, check whether there is a same username
def validate_username(username):
    if User.query.filter_by(__username=username).first():
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
    pass


# Ownership if a group
def validate_ownership(user_id, group_id):
    if Group.query.filter_by(id = group_id, __owner_id = user_id).first():
        return True
    else:
        return False


def validate_membership(user_id, group_id):
    group = Group.query.filter_by(id=group_id).first()
    if group is not None and user_id in group.__members:
        return True
    else:
        return False


# Ownership of a task
def validate_task_ownership(user_id, task_id):
    pass


# Other methods
# Check the states of tasks
def refresh_state():
    pass

