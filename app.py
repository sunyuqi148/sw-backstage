# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import (Flask, request, redirect, url_for)
from flask import json
from flask_login import login_required, login_user, logout_user, current_user

from ext import db, login_manager
from models import User, Group, Task, Validity
import utils

import datetime

app = Flask(__name__)

SECRET_KEY = 'This is my key'
app.secret_key = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@127.0.0.1/test?charset=utf8"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
#db.drop_all(app=app) # Only for debugging
db.create_all(app=app)

login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"


#================ USER FUNCTION =============
## Get info of another user
#@app.route('/get_user', methods=['POST'])
#@login_required
#def get_user():
#    form = {k:request.form[k].strip() for k in request.form}
#    if utils.validate_userid(int(form['user_id'])):
#        user = User.query.filter_by(id=int(form['user_id'])).first()
#        return Validity(True, user.get_map_info())
#    else:
#        return Validity(False, 'Invalid user id').get_resp()


# Update the info of current user
@app.route('/update_user', methods=['POST'])
@login_required
def update_user():
    form = {k:request.form[k].strip() for k in request.form}
    if 'user_id' not in form:
        assert 'user_username' in form
        form['user_id'] = utils.get_userid(form['user_username'])
    current_user.update(username=(None if 'username' not in form else form['username']),
                password=(None if 'password' not in form else form['password']),
                 name=(None if 'name' not in form else form['name']),
                 info=(None if 'info' not in form else form['info']))
    db.session.commit()
    return Validity(True).get_resp()

    
@app.route('/get_friendlist', methods=['GET'])
@login_required
def get_friendlist():
    ret = sorted([friend for friend in current_user.get_friends()])
    ret = [friend.get_info_map() for friend in ret]
    return Validity(True, {'friend list': ret}).get_resp()


@app.route('/get_grouplist', methods=['GET'])
@login_required
def get_grouplist():
    ret = sorted([group for group in current_user.get_groups()])
    ret = [group.get_info_map() for group in ret]
    return Validity(True, {'group list': ret}).get_resp()


# Get all tasks of the user
@app.route('/get_tasklist', methods=['GET'])
@login_required
def get_tasklist():
    ret = sorted([task for task in current_user.get_tasks()])
    ret = [task.get_info_map() for task in ret]
    return Validity(True, {'task list': ret}).get_resp()


# Get public tasks of friends
@app.route('/get_friend_tasklist', methods=['GET'])
@login_required
def get_friend_tasklist():
    ret = []
    for friend in current_user.get_friends():
        ret.extends([task for task in friend.get_public_tasks()])
    ret = sorted(ret)
    ret = [task.get_info_map() for task in ret]
    return Validity(True, {'friend task list': ret}).get_resp()


# Get group tasks of the user
@app.route('/get_group_tasklist', methods=['GET'])
@login_required
def get_group_tasklist():
    ret = []
    for group in current_user.get_groups():
        ret.extends([task for task in group.get_tasks()])
    ret = sorted(ret)
    ret = [task.get_info_map() for task in ret]
    return Validity(True, {'group task list': ret}).get_resp()


@app.route('/add_friend', methods=['POST'])
@login_required
def add_friend():
    form = {k:request.form[k].strip() for k in request.form}
    if 'friend_id' not in form:
        assert 'friend_username' in form
        form['friend_id'] = utils.get_userid(form['friend_username'])
    if not utils.validate_userid(int(form['friend_id'])) or utils.validate_friendship(int(current_user.id), int(form['friend_id'])):
        return Validity(False, 'User ' + form['friend_id'] + ' does not exist.').get_resp()
    friend = User.query.filter_by(id = int(form['friend_id'])).first()
    current_user.add_friend(int(form['friend_id']))
    friend.add_friend(int(current_user.id))
    db.session.commit()
    return Validity(True).get_resp()


@app.route('/delete_friend', methods=['POST'])
@login_required
def delete_friend():
    form = {k:request.form[k].strip() for k in request.form}
    if 'friend_id' not in form:
        assert 'friend_username' in form
        form['friend_id'] = utils.get_userid(form['friend_username'])
    if not utils.validate_userid(int(form['friend_id'])) or not utils.validate_friendship(int(current_user.id), int(form['friend_id'])):
        return Validity(False, 'User ' + form['friend_id'] + ' does not exist.').get_resp()
    friend = User.query.filter_by(id = int(form['friend_id'])).first()
    current_user.delete_friend(int(form['friend_id']))
    friend.delete_friend(int(current_user.id))
    db.session.commit()
    return Validity(True).get_resp()

#================ GROUP FUNCTION =============
# Get info of a group
@app.route('/get_group', methods=['POST'])
@login_required
def get_group():
    form = {k:request.form[k].strip() for k in request.form}
    if utils.validate_groupid(int(form['group_id'])):
#        if utils.validate_membership(current_user.id, int(form['group_id'])):
        group = Group.query.filter_by(id = int(form['group_id'])).first()
        return Validity(True, group.get_map_info())
#        else:
#            return Validity(False, 'No access').get_resp()
    else:
        return Validity(False, 'Invalid group id').get_resp()


# Get group task list
@app.route('/get_group_task', methods=['POST'])
@login_required
def get_group_task():
    form = {k:request.form[k].strip() for k in request.form}
    if utils.validate_groupid(int(form['group_id'])):
        if utils.validate_membership(int(current_user.id), int(form['group_id'])):
            group = Group.query.filter_by(id=int(form['group_id'])).first()
            ret = sorted([task for task in group.get_tasks()])
            ret = [group.get_info_map() for group in ret]
            return Validity(True, {'task list': ret}).get_resp()
        else:
            return Validity(False, 'No access').get_resp()
    else:
        return Validity(False, 'Invalid group id').get_resp()


# Get group member list
@app.route('/get_group_member', methods=['POST'])
@login_required
def get_group_member():
    form = {k:request.form[k].strip() for k in request.form}
    if utils.validate_groupid(int(form['group_id'])):
        if utils.validate_membership(int(current_user.id), int(form['group_id'])):
            group = Group.query.filter_by(id=int(form['group_id'])).first()
            ret = sorted([user for user in group.get_members()])
            ret = [user.get_info_map() for user in ret]
            return Validity(True, {'member list': ret}).get_resp()
        else:
            return Validity(False, 'No access').get_resp()
    else:
        return Validity(False, 'Invalid group id').get_resp()


# Update info of a group
@app.route('/update_group', methods=['POST'])
@login_required
def update_group():
    form = {k:request.form[k].strip() for k in request.form}
    if 'owner_id' not in form:
        assert 'owner_username' in form
        form['owner_id'] = utils.get_userid(form['owner_username'])
    if utils.validate_groupid(int(form['group_id'])):
        if utils.validate_ownership(int(current_user.id), int(form['group_id'])):
            group = Group.query.filter_by(id = int(form['group_id'])).first()
            group.update(name=(None if 'name' not in form else form['name']),
                         owner_id=(None if 'owner_id' not in form else int(form['owner_id'])),
                         info=(None if 'info' not in form else form['info']))
            db.session.commit()
            return Validity(True).get_resp()
        else:
            return Validity(False, 'No access').get_resp()
    else:
        return Validity(False, 'Invalid group id').get_resp()


# Create group task
@app.route('/create_group_task', methods=['POST'])
@login_required
def create_group_task():
    form = {k:request.form[k].strip() for k in request.form}
    if utils.validate_ownership(int(current_user.id), int(form['group_id'])):
        task = Task(owner_id=int(current_user.id),
                    title=form['title'],
                    finish_time=utils.trans_to_date(form['deadline']),
                    status=(0 if 'status' not in form else form['status']),
                    publicity=2,
                    group_id=(None if 'group_id' not in form else int(form['group_id'])),
                    info=('' if 'info' not in form else form['info']))
        db.session.add(task)
        db.session.commit()
        return Validity(True, task.get_info_map()).get_resp()
    else:
        return Validity(False, 'No access').get_resp()


# Update group task
@app.route('/update_group_task', methods=['POST'])
@login_required
def update_group_task():
    form = {k:request.form[k].strip() for k in request.form}
    if utils.validate_taskid(int(form['task_id'])):
        task = Task.query.filter_by(int(form['task_id'])).first()
        if utils.validate_ownership(int(current_user.id), int(form['group_id'])):
            task.update(owner_id=None,
                        title=(None if 'title' not in form else form['title']),
                        finish_time=(None if 'finish_time' not in form else utils.trans_to_date(form['finish_time'])),
                        status=(None if 'status' not in form else form['status']),
                        publicity=(None if 'publicity' not in form else int(form['publicity'])),
                        group_id=(None if 'group_id' not in form else int(form['group_id'])),
                        info=(None if 'info' not in form else form['info']))
            return Validity(True).get_resp()
        elif utils.validate_membership(int(current_user.id), int(form['group_id'])):
            # members can only edit the progress
            task.update(status=(None if 'status' not in form else int(form['status'])))
            return Validity(True).get_resp()
        else:
            return Validity(False, 'No access').get_resp()
    else:
        return Validity(False, 'Invalid task id').get_resp()


# Delete group task
@app.route('/delete_group_task', methods=['POST'])
@login_required
def delete_group_task():
    form = {k:request.form[k].strip() for k in request.form}
    if utils.validate_ownership(int(current_user.id), int(form['group_id'])):
        if Task.query.filter_by(id=int(form['task_id'])).first():
            task = Task.query.filter_by(id=int(form['task_id'])).first()
            db.session.delete(task)
            db.session.commit()
            return Validity(True).get_resp()
        else:
            return Validity(False, 'Invalid task id').get_resp()
    else:
        return Validity(False, 'No access').get_resp()
    

# Create a group
@app.route('/create_group', methods=['POST'])
@login_required
def create_group():
    form = {k:request.form[k].strip() for k in request.form}
    group = Group(name=form['name'],
                  owner_id=int(current_user.id),
                  info=('' if 'info' not in form else form['info']))
    db.session.add(group)
    db.session.commit()
    print('group created')
    return Validity(True, group.get_info_map()).get_resp()


# Delete a group
@app.route('/delete_group', methods=['POST'])
@login_required
def delete_group():
    form = {k:request.form[k].strip() for k in request.form}
    if utils.validate_groupid(group_id=int(form['group_id'])):
        if utils.validate_ownership(int(current_user.id), int(form['group_id'])):
            group = Group.query.filter_by(id=int(form['group_id'])).first()
            db.session.delete(group)
            db.session.commit()
            return Validity(True).get_resp()
        else:
            return Validity(False, 'No access').get_resp()
    else:
        return Validity(False, 'Invalid group id').get_resp()


# Join a group
@app.route('/join_group', methods=['POST'])
@login_required
def join_group():
    form = {k:request.form[k].strip() for k in request.form}
    if utils.validate_groupid(group_id=int(form['group_id'])):
        if not utils.validate_membership(int(current_user.id), int(form['group_id'])):
            group = Group.query.filter_by(id=int(form['group_id'])).first()
            group.add_member(int(current_user.id))
            db.session.commit()
            return Validity(True).get_resp()
        else:
            return Validity(False, 'Already in the group').get_resp()
    else:
        return Validity(False, 'Invalid group id').get_resp()


# Quit a group
@app.route('/quit_group', methods=['POST'])
@login_required
def quit_group():
    form = {k:request.form[k].strip() for k in request.form}
    if utils.validate_groupid(group_id=int(form['group_id'])):
        if utils.validate_membership(int(current_user.id), int(form['group_id'])) and not utils.validate_ownership(int(current_user.id), int(form['group_id'])):
            group = Group.query.filter_by(id=int(form['group_id'])).first()
            group.delete_member(int(current_user.id))
            db.session.commit()
            return Validity(True).get_resp()
        else:
            return Validity(False, 'Can not quit the group').get_resp()
    else:
        return Validity(False, 'Invalid group id').get_resp()


# Add a member to the group
@app.route('/add_member', methods=['POST'])
@login_required
def add_member():
    form = {k:request.form[k].strip() for k in request.form}
    if 'user_id' not in form:
        assert 'user_username' in form
        form['user_id'] = utils.get_userid(form['user_username'])
    if utils.validate_groupid(group_id=int(form['group_id'])):
        if not utils.validate_membership(int(form['user_id']), int(form['group_id'])):
            group = Group.query.filter_by(id=int(form['group_id'])).first()
            group.add_member(int(form['user_id']))
            db.session.commit()
            return Validity(True).get_resp()
        else:
            return Validity(False, 'Already in the group').get_resp()
    else:
        return Validity(False, 'Invalid group id').get_resp()


# Delete a member from the group
@app.route('/delete_member', methods=['POST'])
@login_required
def delete_member():
    form = {k:request.form[k].strip() for k in request.form}
    if 'user_id' not in form:
        assert 'user_username' in form
        form['user_id'] = utils.get_userid(form['user_username'])
    if utils.validate_groupid(group_id=int(form['group_id'])):
        if utils.validate_membership(int(form['user_id']), int(form['group_id'])) and not utils.validate_ownership(int(form['user_id']), int(form['group_id'])):
            group = Group.query.filter_by(id=int(form['group_id'])).first()
            group.delete_member(int(form['user_id']))
            db.session.commit()
            return Validity(True).get_resp()
        else:
            return Validity(False, 'Can not quit the group').get_resp()
    else:
        return Validity(False, 'Invalid group id').get_resp()


#================== Task SubSystem ==================

# Get task info
@app.route('/get_task', methods=['POST'])
@login_required
def get_task():
    form = {k:request.form[k].strip() for k in request.form}
    if utils.validate_taskid(int(form['task_id'])):
        task = Task.query.filter_by(id=int(form['task_id'])).first()
        return Validity(True, task.get_map_info())
    else:
        return Validity(False, 'Invalid task id').get_resp()
    

#@app.route('/get_tasklist', methods=['GET'])
#@login_required
#def get_tasklist(): # TODO(interaction): For test, implement it correctely
#    tasklist = Task.query.filter_by(__owner_id=current_user.get_id()).all()
##    tasklist = [Task(0, 'test1', datetime.datetime.now()), Task(1, 'test2', datetime.datetime.now())] # For test
#    ret = []
#    for task in tasklist:
#        ret.append(task.get_info_map())
#    return Validity(True, {'task': ret}).get_resp() 
#    #'get tasklist.'#Task.query.filter_by(id=int(user_id)).first()
#    #User.get_tasklist_resp(user_id=int(current_user.id))


# Update task info, include finishing the task
@app.route('/update_task', methods=['POST'])
@login_required
def update_task():
    form = {k:request.form[k].strip() for k in request.form}
    if utils.validate_taskid(int(form['task_id'])):
        if utils.validate_task_ownership(int(current_user.id), int(form['task_id'])):
            task = Task.query.filter_by(id=int(form['task_id'])).first()
            task.update(# owner_id=None, # I don't think any user have the authority to change task's owner
                        title=(None if 'title' not in form else form['title']),
                        finish_time=(None if 'finish_time' not in form else utils.trans_to_date(form['finish_time'])),
                        status=(None if 'status' not in form else form['status']),
                        publicity=(None if 'publicity' not in form else int(form['publicity'])),
                        group_id=(None if 'group_id' not in form else int(form['group_id'])),
                        info=(None if 'info' not in form else form['info']))
            db.session.commit()
            return Validity(True).get_resp()
        else:
            return Validity(False, 'No access').get_resp()
    else:
        return Validity(False, 'Invalid task id').get_resp()


#@app.route('/finish_task', methods=['POST'])
#@login_required
#def finish_task():
#    if Task.finish_task(user_id=int(current_user.id), task_id=int(form['task_id'])):
#        return Validity(True).get_resp()
#    else:
#        return Validity(False, 'Invalid task id').get_resp()


@app.route('/create_task', methods=['POST'])
@login_required
def create_task():
    form = {k:request.form[k].strip() for k in request.form}
    print(current_user.id)
    print(form)
    task = Task(owner_id=int(current_user.id),
                title=form['title'],
                finish_time=(datetime.datetime.now() if 'deadline' not in form else utils.trans_to_date(form['deadline'])),
                status=(0 if 'status' not in form else form['status']),
                publicity=(0 if 'publicity' not in form else form['publicity']),
                group_id=(None if 'group_id' not in form else form['group_id']),
                info=('' if 'info' not in form else form['info']))
    db.session.add(task)
    db.session.commit()
    return Validity(True, task.get_info_map()).get_resp()


@app.route('/delete_task', methods=['POST'])
@login_required
def delete_task():
    form = {k:request.form[k].strip() for k in request.form}
    if Task.validate_task_id(task_id=int(form['task_id'])):
        task = Task.query.filter_by(id=int(form['task_id'])).first()
        db.session.delete(task)
        db.session.commit()
        return Validity(True).get_resp()
    else:
        return Validity(False, 'Invalid task id').get_resp()


#================== User SubSystem (tested) ==================

@app.route('/register', methods=['GET','POST'])
def register():
    form = {k:request.form[k].strip() for k in request.form}
    print(form['username'], form['password'])
    if utils.validate_username(form['username']):
        user = User(username=form['username'],
                    password=form['password']
                    )
        db.session.add(user)
        db.session.commit()
        # login_user(user, remember=True)
        print('valid')
        return Validity(True).get_resp() # 'register succeeds'
    else:
        print('invalid')
        return Validity(False, 'Register fails: Invalid username or password.').get_resp() # 'register fails'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = {k:request.form[k].strip() for k in request.form}
    print(form['username'], form['password'])
    user = User.query.filter_by(username=form['username'],
                                password=form['password']
                                ).first()
    if user:
        login_user(user, remember=True)
        return Validity(True).get_resp()#redirect(url_for('get_tasklist')) #json.dumps({'valid': True, 'task': ret}) #'login succeeds'
    else:
        return Validity(False, 'Login fails: Invalid username or password.').get_resp() #'login fails'


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return Validity(True).get_resp()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()
    


#================== Test ==================

@app.route('/', methods=['GET', 'POST'])
def test():
    user = User(username='管理员', password='admin')
    db.session.add(user)
#    user = User(username='admin1', password='admin1')
#    db.session.add(user)
#    user = User(username='admin2', password='admin2')
#    db.session.add(user)
    db.session.commit()
#    task = Task(1, 'ok', datetime.datetime.now())
#    db.session.add(task)
#    task = Task(1, 'ok1', datetime.datetime.now())
#    db.session.add(task)
#    db.session.commit()
#    user1 = User.query.filter_by(id=1).first()
#    user2 = User.query.filter_by(id=2).first()
#    user1.add_friend(2)
#    print(user1.get_friends())
#    print(user2.get_friends())
#    db.session.commit()
#    group = Group('test group', owner_id=1)
#    db.session.add(group)
#    group.add_member(2)
#    db.session.commit()
#    print(user1.get_ownership())
#    print(group.get_members())
#    print(user2.get_groups())
    
#    print(User.query.filter_by(id=1).first().__friends)
#    print(User.query.filter_by(id=2).first().__friends)
#    print(user.tasks)
#    login_user(user1, remember=True)
#    print('logged in as ' + current_user.username)
#    print([task.get_info_map() for task in current_user.get_tasks()])
#    logout_user()
#    print([task.get_info_map() for task in current_user.get_tasks()])
#    print('logged in as ' + current_user.username)
    
    return 'successful!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True, ssl_context='adhoc')
#    app.run(host='127.0.0.1', port=5000, debug=True)
    
