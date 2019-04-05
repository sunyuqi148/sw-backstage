from flask import (Flask, request)
from flask import json
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from models import User, TodoList, Validity

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/login', methods=['POST'])
def login():
	user = User.get_id(username=request.form['username'], password=request.form['password'])
	if user:
		login_user(user)
		todolist = User.get_todolist(user)
		return todolist.get_resp()
	else:
		return Validity(False).get_resp() #TODO: login invalid username or passwd


@app.route('/logout')
@login_required
def logout():
	logout_user()
	return Validity(True).get_resp() #TODO: logout succeeded


@login_manager.user_loader
def load_user(user_id):
	return User.get(user_id)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)
