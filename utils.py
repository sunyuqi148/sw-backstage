# -*- coding: utf-8 -*-
from models import User, Group, Task

# Validating methods
def validate_userid(user_id):
    if User.query.filter_by(id=user_id).first():
        return False
    else:
        return True


def validate_username(username):
    if User.query.filter_by(username=username).first():
        return False
    else:
        return True


def validate_groupid(group_id):
    if Group.query.filter_by(id=group_id).first():
        return False
    else:
        return True


def validate_taskid(task_id):
    if Task.query.filter_by(id=task_id).first():
        return False
    else:
        return True


def validate_friendship(user_id, friend_id):
    pass


# Ownership if a group
def validate_ownership(user_id, group_id):
    pass


def validate_membership(user_id, group_id):
    pass


# Ownership if a task
def validate_task_ownership(user_id, task_id):
    pass


# Other methods
# Check the states of tasks
def refresh_state():
    pass

