# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from flask import (Flask, request, flash, redirect, url_for)
from flask import json
from flask_login import login_required, login_user, logout_user, current_user
#from flask_sqlalchemy import SQLAlchemy

from ext import db, login_manager
from models import User, Group, Task, Validity
from utils import validate_username

import datetime

app = Flask(__name__)

SECRET_KEY = 'This is my key'
app.secret_key = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:root@127.0.0.1/test"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)
db.drop_all(app=app)
db.create_all(app=app)

login_manager.init_app(app)
login_manager.login_view = "login"


@app.route('/addfriend', methods=['POST'])
@login_required
def add_friend():
    friend_id = User.get_friend_id(username=request.form['friend_username'])
    if friend_id:
        if not User.add_friend(user_id=current_user.id, friend_id=friend_id):
            return Validity(False, 'Friend already exists in your friend list.').get_resp()
        return User.get_friendlist_resp(user_id=current_user.id)
    else:
        return Validity(False, 'User ' + request.form['friend_username'] + ' does not exist.').get_resp()


@app.route('/getfriend', methods=['GET'])
@login_required
def get_friend():
    return User.get_friendlist_resp(user_id=current_user.id)


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


@app.route('/addtask', methods=['POST'])
@login_required
def add_task():
    task = Task(user_id=current_user.id,
				title=request.form['title'],
				deadline=request.form['deadline'],
				description=request.form['description'])
    return task.get_resp()
	
	
@app.route('/modifytask', methods=['POST'])
@login_required
def modify_task():
    task = Task.get_task(user_id=current_user.id, task_id=request.form['task_id'])
    if task:
        if 'title' in request.form: task.modify_title(request.form['title'])
        if 'deadline' in request.form: task.modify_deadline(request.form['deadline'])
        if 'description' in request.form: task.modify_description(request.form['description'])
        return Validity(True).get_resp()
    else:
        return Validity(False, 'Invalid task id').get_resp()

@app.route('/deletetask', methods=['POST'])
@login_required
def delete_task():
    if Task.delete_task(user_id=current_user.id, task_id=request.form['task_id']):
        return Validity(True).get_resp()
    else:
        return Validity(False, 'Invalid task id').get_resp()


@app.route('/finishtask', methods=['POST'])
@login_required
def finish_task():
    if Task.finish_task(user_id=current_user.id, task_id=request.form['task_id']):
        return Validity(True).get_resp()
    else:
        return Validity(False, 'Invalid task id').get_resp()
	
	
@app.route('/refresh_todolist')
@login_required
def refresh_todolist():
    return Task.get_todolist_resp(current_user.id)


@app.route('/index', methods=['GET'])
@login_required
def index():
    return 'you have logined as ' + current_user.username


import random # Only for test @_@
@app.route('/register', methods=['GET','POST'])
def register():
    print("register called")
    username='zhanghaix'+str(random.randint(0,500)) # Only for test @_@
    if not validate_username(username):
        return 'username already exists!'
    password='zhanghaix'
    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()
    login_user(user, remember=True)
    next = request.args.get('next')
    return redirect(next or url_for('login'))
#    return redirect(url_for('index'))
#    user_id = User.register_user(username=request.form['username'], password=request.form['password'])
#    if user_id:
#        return User.get_resp(user_id)
#    else:
#        return Validity(False, 'Username already exists or invalid password.').get_resp()


@app.route('/login', methods=['GET', 'POST'])
def login():
    user = User.query.filter_by(username='zhanghaix', password='zhanghaix').first()
    if user:
        login_user(user, remember=True)
        next = request.args.get('next')
        return redirect(next or url_for('index'))
    else:
        return 'Login failed!'
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
    return redirect(url_for('login'))
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
    app.run(host='127.0.0.1', port=5000, debug=True)
    
