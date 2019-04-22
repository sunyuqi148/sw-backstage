# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import (Flask, request)
from flask import json
from flask_login import login_required, login_user, logout_user, current_user

from ext import db, login_manager
from models import User, Group, Task, validate_username
from utils import Validity

import datetime

app = Flask(__name__)

SECRET_KEY = 'This is my key'
app.secret_key = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@127.0.0.1/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
#db.drop_all(app=app)
db.create_all(app=app)

login_manager.init_app(app)
login_manager.login_view = "login"


# Update the info of current user
@app.route('/update_info', methods=['POST'])
@login_required
def update_info():
    pass # TODO


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


@app.route('/get_friendlist', methods=['GET'])
@login_required
def get_friendlist():
    return User.get_friendlist_resp(user_id=current_user.id)


@app.route('/get_tasklist', methods=['GET'])
@login_required
def get_tasklist():
    return User.get_tasklist_resp(user_id=current_user.id)


# Get info of another user
@app.route('/get_friend', methods=['POST'])
@login_required
def get_friend():
    pass # TODO


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


@app.route('/create_task', methods=['POST'])
@login_required
def create_task():
    task = Task(user_id=current_user.id,
				title=request.form['title'],
				deadline=request.form['deadline'],
				description=request.form['description'])
    return task.get_resp()
	
	
# Include: get task info, finish task and update task
@app.route('/get_task', methods=['POST'])
@login_required
def get_task():
    task = Task.get_task(user_id=current_user.id, task_id=request.form['task_id'])
    if task:
        if 'title' in request.form: task.modify_title(request.form['title'])
        if 'deadline' in request.form: task.modify_deadline(request.form['deadline'])
        if 'description' in request.form: task.modify_description(request.form['description'])
        return Validity(True).get_resp()
    else:
        return Validity(False, 'Invalid task id').get_resp()


@app.route('/delete_task', methods=['POST'])
@login_required
def delete_task():
    if Task.delete_task(user_id=current_user.id, task_id=request.form['task_id']):
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
	
	
# Refreshing: check any updates on dataset and renew status of tasks
@app.route('/refresh')
@login_required
def refresh():
    return Task.get_tasklist_resp(current_user.id)


# Create a new group
@app.route('/create_group', methods=['POST'])
@login_required
def create_group():
    pass # TODO


# Create a new group
@app.route('/join_group', methods=['POST'])
@login_required
def join_group():
    pass # TODO


# Include: get info of a group and update info of a group
@app.route('/get_group', methods=['POST'])
@login_required
def get_group():
    pass # TODO


# Include quit a group and delete a whole group
@app.route('/delete_group', methods=['POST'])
@login_required
def delete_group():
    pass # TODO


@app.route('/register', methods=['GET','POST'])
def register():
    if validate_username(request.form['username']):
        user = User(username=request.form['username'],
                    password=request.form['password'],
                    name=request.form['name'],
                    info=request.form['info']
                    )
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return 'register succeeds'
    else:
        return 'register fails'
#    user_id = User.register_user(username=request.form['username'], password=request.form['password'])
#    if user_id:
#        return User.get_resp(user_id)
#    else:
#        return Validity(False, 'Username already exists or invalid password.').get_resp()


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = User.query.filter_by(username=request.form['username'],
                                password=request.form['password']
                                ).first()
    if user:
        login_user(user, remember=True)
        return 'login succeeds'
    else:
        return 'login fails'
#    user_id = User.get_id(username=request.form['username'], password=request.form['password'])
#    if user_id:
#        login_user(user_id)
#        return Task.get_todolist_resp(user_id) 
#    else:
#        return Validity(False, 'Invalid username or password.').get_resp()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'logout succeeds'
#    return Validity(True).get_resp()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=int(user_id)).first()


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
    user1.friends.extend([user2,user3])
    db.session.commit()
    print(User.query.filter_by(id=1).first().friends)
    print(User.query.filter_by(id=2).first().friends)
#    print(user.tasks)
    return 'successful!'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=False, ssl_context='adhoc')
    
