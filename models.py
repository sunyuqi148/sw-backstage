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

	# rets: user_id (if valid)
	#       False (if invalid)
	def register_user(username, password):
		pass

	# rets: json map includes valid=true and user_id
	def get_resp():
		pass
		
		

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
	
	def __init__(user_id, title, deadline, description):
		pass
	
	# rets: a json string of all tasks belonging to user
	def get_todolist_resp(user_id):
		pass
						
	# Generates response including task id, valid = True
	def get_resp():
		pass
		
	# returns NULL if task_id is invalid.
	def get_task(user_id, task_id):
		pass
		
	def delete_task(user_id, task_id):
		pass
	
	def finish_task(user_id, task_id):
		pass
	
	def modify_title():
		pass
	
	def modify_deadline():
		pass
	
	def modify_description():
		pass
	