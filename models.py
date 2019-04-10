from flask import json
from flask.ext.login import UserMixin

## These classes should inherit flask.ext.login.UserMixin.
## See: https://flask-login.readthedocs.io/en/latest/
##      or 
##      https://www.cnblogs.com/agmcs/p/4445428.html

class User(UserMixin):
	# args: username, password
	# rets: user_id (if valid)
	#		False (if invalid)
	def get_id(username, password):
		pass # TODO: implement this function
	
	# args: user_id
	def get(user_id):
		pass # TODO: implement this function
	
	# args: user_id
	# rets: todolist
	def get_todolist():
		pass # TODO: implement this function
		
	# args: task_id
	# rets: task
	def get_task():
		pass # TODO: implement this function

	# Adds a task to this user's todolist
	# args: task
	def add_task():
		pass # TODO: implement this function
	
	# Deletes a task from user's todolist
	# args: task_id
	# rets: True if task_id is valid and user has authority, else False
	def delete_task():
		pass # TODO: implement this function
		
	# Sets task as finished 
	# args: task_id
	# rets: True if task_id is valid and user has authority, else False
	def finish_task():
		pass # TODO: implement this function

class TodoList:
	# rets: a json string of todolist, valid = True
	def get_resp():
		pass # TODO: implement this function
	
class Validity:
	# args: valid
	def __init__(valid = False,
				 info = ''):
		self._valid = valid
		self._info = info
	
	# rets: a json string of validity
	def get_resp():
		return Response(json.dumps({'valid': self._valid,
									'info': self._info}),
						content_type='application/json')
		
		
class Task:
	# title, deadline, desciption, task_id, user_id(maybe)
	
	# Generates response including task id, valid = True
	def get_resp():
		pass
	
	def modify_title():
		pass
	
	def modify_deadline():
		pass
	
	def modify_description():
		pass
	