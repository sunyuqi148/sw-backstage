from flask import (Flask, request)
from flask import json
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import User, Task, TodoList, Validity

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)


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
		if not User.delete_friend(user_id=current_user.id, friend_id=friend_id)
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
	else :
		return Validity(False, 'Invalid task id').get_resp()


@app.route('/finishtask', methods=['POST'])
@login_required
def finish_task():
	if Task.finish_task(user_id=current_user.id, task_id=request.form['task_id']):
		return Validity(True).get_resp()
	else :
		return Validity(False, 'Invalid task id').get_resp()
	
	
@app.route('/refresh_todolist')
@login_required
def refresh_todolist():
	return Task.get_todolist_resp(current_user.id)


@app.route('/login', methods=['POST'])
def login():
	user_id = User.get_id(username=request.form['username'], password=request.form['password'])
	if user_id:
		login_user(user_id)
		return Task.get_todolist_resp(user_id)
	else:
		return Validity(False, 'Invalid username or password.').get_resp()


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return Validity(True).get_resp()


@login_manager.user_loader
def load_user(user_id):
	return User.get(user_id=user_id)
	

@app.route('register', methods=['POST'])
def register():
	user_id = User.register_user(username=request.form['username'], password=request.form['password'])
	if user_id:
		return User.get_resp(user_id)
	else:
		return Validity(False, 'Username already exists or invalid password.').get_resp()


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)
