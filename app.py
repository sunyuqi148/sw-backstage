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

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@127.0.0.1/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
db.drop_all(app=app) # Only for debugging
db.create_all(app=app)

login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"


# Get info of another user
@app.route('/get_user', methods=['POST'])
@login_required
def get_user():
    pass # TODO


# Update the info of current user
@app.route('/update_user', methods=['POST'])
@login_required
def update_user():
    pass # TODO


# Refreshing: check any updates on dataset and renew status of tasks
@app.route('/refresh')
@login_required
def refresh():
    #pass # TODO
    print(current_user)
    print(current_user.is_anonymous)
    return current_user.get_resp()
    
@app.route('/get_friendlist', methods=['GET'])
@login_required
def get_friendlist():
    return User.get_friendlist_resp(user_id=current_user.id)



@app.route('/get_friend_tasklist', methods=['GET'])
@login_required
def get_friend_tasklist():
    return User.get_friend_tasklist_resp(user_id=current_user.id)


@app.route('/get_group_tasklist', methods=['GET'])
@login_required
def get_group_tasklist():
    return User.get_group_tasklist_resp(user_id=current_user.id)


@app.route('/add_friend', methods=['POST'])
@login_required
def add_friend():
    friend_id = User.get_friend_id(username=request.form['friend_username'])
    if friend_id:
        if not User.add_friend(user_id=current_user.id, friend_id=friend_id):
            return Validity(False, 'Friend already exists in your friend list.').get_resp()
        return User.get_friendlist_resp(user_id=current_user.id)
    else:
        return Validity(False, 'User ' + request.form['friend_username'] + ' does not exist.').get_resp()


@app.route('/delete_friend', methods=['POST'])
@login_required
def delete_friend():
    friend_id = User.get_friend_id(username=request.form['friend_username'])
    if friend_id:
        if not User.delete_friend(user_id=current_user.id, friend_id=friend_id):
            return Validity(False, 'Invalid friend id.').get_resp()
        return Validity(True).get_resp()
    else:
        return Validity(False, 'User ' + request.form['friend_username'] + ' does not exist.').get_resp()

#================ GROUP FUNCTION =============
# Get info of a group
@app.route('/get_group', methods=['POST'])
@login_required
def get_group():
    if utils.validate_groupid(request.form['group_id']):
        if utils.validate_membership(current_user.id, request.form['group_id']):
            group = Group.query.filter_by(id = request.form['group_id'])
            return  Validity(True, ret_map=group.get_map_info())
        else:
            return Validity(False, 'No access').get_resp()
    else:
        return Validity(False, 'Invalid group id').get_resp()


# Get group task list
@app.route('/get_group_task', methods=['POST'])
@login_required
def get_group_task():
    if utils.validate_groupid(request.form['group_id']):
        if utils.validate_membership(current_user.id, request.form['group_id']):
            tasklist = Task.query.filter_by(_group_id = request.form['group_id']).all()
            ret = []
            for task in tasklist:
                ret.append(task.get_info_map())
            return Validity(True, {'task': ret}).get_resp()
        else:
            return Validity(False, 'No access').get_resp()
    else:
        return Validity(False, 'Invalid group id').get_resp()


# Get group member list
@app.route('/get_group_member', methods=['POST'])
@login_required
def get_group_member():
    if utils.validate_groupid(request.form['group_id']):
        if utils.validate_membership(current_user.id, request.form['group_id']):
            group = Group.query.filter_by(id = request.form['group_id'])
            members = group.get_members()
            ret = []
            for member in members:
                ret.append(member.get_info_map())
            return Validity(True, {'member list': ret}).get_resp()
        else:
            return Validity(False, 'No access').get_resp()
    else:
        return Validity(False, 'Invalid group id').get_resp()


# Update info of a group
@app.route('/update_group', methods=['POST'])
@login_required
def update_group():
    if utils.validate_groupid(request.form['task_id']):
        if utils.validate_ownership(current_user.id, request.form['group.id']):
            group = Group.query.filter_by(id = request.form['group_id'])
            group.update(name=(None if 'name' not in request.form else request.form['name']),
                         owner_id=(None if 'owner_id' not in request.form else request.form['owner_id']),
                         info=('' if 'info' not in request.form else request.form['info']))
            return Validity(True).get_resp()
    else:
        return Validity(False, 'Invalid group id').get_resp()

# Check the ownership of a group
@app.route('/check_ownership',methods=['POST'])
@login_required
def check_ownership():
    if utils.validate_ownership(current_user.id, request.form['group.id']):
        return Validity(True).get_resp()
    else:
        return Validity(False).get_resp()

# Create group task
@app.route('/create_group_task', methods=['POST'])
@login_required
def create_group_task():
    if utils.validate_ownership(current_user.id, request.form['group.id']):
        form = request.form
        task = Task(owner_id=current_user.id,
                    title=form['title'],
                    finish_time=form['deadline'],
                    status=(0 if 'status' not in form else form['status']),
                    publicity=(0 if 'publicity' not in form else form['publicity']),
                    group_id=(None if 'group_id' not in form else form['group_id']),
                    info=('' if 'info' not in form else form['info']))
        db.session.add(task)
        db.commit()
        return Validity(True, task.get_info_map()).get_resp()
    else:
        return Validity(False, 'No access').get_resp()


# Update group task
@app.route('/update_group_task', methods=['POST'])
@login_required
def update_group_task():
    if utils.validate_taskid(request.form['task_id']):
        task = Task.query.filter_by(request.form['task_id'])
        if utils.validate_membership(current_user.id, request.form['group_id']):
            # members can only edit the progress
            task.update(owner_id=None,
                        title=None,
                        finish_time=None,
                        status=(None if 'status' not in request.form else request.form['status']),
                        publicity=None,
                        group_id=None,
                        info='')
            return Validity(True).get_resp()
        if utils.validate_ownership(current_user.id, request.form['group_id']):
            task.update(owner_id=None,
                        title=(None if 'title' not in request.form else request.form['title']),
                        finish_time=(None if 'finish_time' not in request.form else request.form['finish_time']),
                        status=(None if 'status' not in request.form else request.form['status']),
                        publicity=(None if 'publicity' not in request.form else request.form['publicity']),
                        group_id=(None if 'group_id' not in request.form else request.form['group_id']),
                        info=('' if 'info' not in request.form else request.form['info']))
            return Validity(True).get_resp()
        else:
            return Validity(False, 'Invalid task id').get_resp()
    else:
        return Validity(False, 'No access').get_resp()


# Delete group task
@app.route('/delete_group_task', methods=['POST'])
@login_required
def delete_group_task():
    if utils.validate_ownership(current_user.id, request.form['group_id']):
        if Task.validate_task_id(task_id=request.form['task_id']):
            task = Task.query.filter_by(id=request.form['task_id'])
            db.session.delete(task)
            db.commit()
            return Validity(True).get_resp()
        else:
            return Validity(False, 'Invalid task id').get_resp()
    else:
        return Validity(False, 'No access').get_resp()
    

# Create a group
@app.route('/create_group', methods=['POST'])
@login_required
def create_group():
    form = request.form
    group = Group(name=form['name'],
                  owner_id=current_user.id,
                  info=('' if 'info' not in form else form['info']))
    db.session.add(group)
    db.commit()
    print('group created')
    return Validity(True, group.get_info_map()).get_resp()


# Delete a group
@app.route('/delete_group', methods=['POST'])
@login_required
def delete_group():
    if utils.validate_groupid(group_id=request.form['group_id']):
        if utils.validate_ownership(current_user.id, request.form['group_id']):
            group = Group.query.filter_by(id=request.form['group_id'])
            db.session.delete(group)
            db.commit()
            return Validity(True).get_resp()
        else:
            return Validity(False, 'No access').get_resp()
    else:
        return Validity(False, 'Invalid task id').get_resp()


# Join a group
@app.route('/join_group', methods=['POST'])
@login_required
def join_group():
    pass  # TODO


# Quit a group
@app.route('/quit_group', methods=['POST'])
@login_required
def quit_group():
    pass  # TODO


# Add a member to the group
@app.route('/add_member', methods=['POST'])
@login_required
def add_member():
    pass  # TODO


# Delete a member from the group
@app.route('/delete_member', methods=['POST'])
@login_required
def delete_member():
    pass  # TODO


#================== Task SubSystem ==================

# Get task info
@app.route('/get_task', methods=['POST'])
@login_required
def get_task():
    #TODO(database): finished Task or utils, validate_taskid(), validate the task_id for logined user.
    if utils.validate_taskid(current_user.id, request.form['task_id']):
        task = Task.get(request.form['task_id'])
        return Validity(True, ret_map=task.get_map_info())
    else:
        return Validity(False, 'Invalid task id').get_resp()
    

@app.route('/get_tasklist', methods=['GET'])
@login_required
def get_tasklist(): # TODO(interaction): For test, implement it correctely
    #TODO(database): finished
    tasklist = Task.query.filter_by(__owner_id=current_user.get_id()).all()
#    tasklist = [Task(0, 'test1', datetime.datetime.now()), Task(1, 'test2', datetime.datetime.now())] # For test
    ret = []
    for task in tasklist:
        ret.append(task.get_info_map())
    return Validity(True, {'task': ret}).get_resp() 
    #'get tasklist.'#Task.query.filter_by(id=int(user_id)).first()
    #User.get_tasklist_resp(user_id=current_user.id)


# Update task info, include finishing the task
@app.route('/update_task', methods=['POST'])
@login_required
def update_task():
    if Task.validate_task_id(current_user.id, request.form['task_id']):
        Task.update(owner_id=None, # I don't think any user have the authority to change task's owner
                    title=(None if 'title' not in form else form['title']),
                    finish_time=(None if 'finish_time' not in form else form['finish_time']),
                    status=(None if 'status' not in form else form['status']),
                    publicity=(None if 'publicity' not in form else form['publicity']),
                    group_id=(None if 'group_id' not in form else form['group_id']),
                    info=('' if 'info' not in form else form['info']))
        return Validity(True).get_resp()
    else:
        return Validity(False, 'Invalid task id').get_resp()


#@app.route('/finish_task', methods=['POST'])
#@login_required
#def finish_task():
#    if Task.finish_task(user_id=current_user.id, task_id=request.form['task_id']):
#        return Validity(True).get_resp()
#    else:
#        return Validity(False, 'Invalid task id').get_resp()


@app.route('/create_task', methods=['POST'])
@login_required
def create_task():
    form = request.form
    task = Task(owner_id=current_user.id,
                title=form['title'],
                finish_time=form['deadline'],
                status=(0 if 'status' not in form else form['status']),
                publicity=(0 if 'publicity' not in form else form['publicity']),
                group_id=(None if 'group_id' not in form else form['group_id']),
                info=('' if 'info' not in form else form['info']))
    db.session.add(task) #TODO(database): add a task finished
    db.commit()
    return Validity(True, task.get_info_map()).get_resp()


@app.route('/delete_task', methods=['POST'])
@login_required
def delete_task():
    if Task.validate_task_id(task_id=request.form['task_id']):
        #TODO(database): delete a task finished
        task = Task.query.filter_by(id=request.form['task_id'])
        db.session.delete(task)
        db.commit()
        return Validity(True).get_resp()
    else:
        return Validity(False, 'Invalid task id').get_resp()


#================== User SubSystem (tested) ==================

@app.route('/register', methods=['GET','POST'])
def register():
    print(request.form['username'], request.form['password'])
    if utils.validate_username(request.form['username']):
        user = User(username=request.form['username'],
                    password=request.form['password']
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
    print(request.form['username'], request.form['password'])
    user = User.query.filter_by(__username=request.form['username'],
                                __password=request.form['password']
                                ).first()
    if user:
        login_user(user, remember=True)
        return redirect(url_for('get_tasklist')) #json.dumps({'valid': True, 'task': ret}) #'login succeeds'
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
    user = User(username='admin', password='admin')
    db.session.add(user)
    user = User(username='admin1', password='admin1')
    db.session.add(user)
    user = User(username='admin2', password='admin2')
    db.session.add(user)
#    db.session.commit()
    task = Task(1, 'ok', datetime.datetime.now())
    db.session.add(task)
    task = Task(1, 'ok1', datetime.datetime.now())
    db.session.add(task)
    db.session.commit()
#    group = Group('test_group', 1)
    user1 = User.query.filter_by(id=1).first()
    user2 = User.query.filter_by(id=2).first()
    user3 = User.query.filter_by(id=3).first()
    user1.__friends.extend([user2,user3])
    db.session.commit()
    print(User.query.filter_by(id=1).first().__friends)
    print(User.query.filter_by(id=2).first().__friends)
#    print(user.tasks)
    return 'successful!'


if __name__ == "__main__":
#    app.run(host='0.0.0.0', port=80, debug=False, ssl_context='adhoc')
    app.run(host='127.0.0.1', port=5000, debug=True)
    
