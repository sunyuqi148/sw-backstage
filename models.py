from flask import json


## These classes should inherit flask.ext.login.UserMixin.
## See: https://flask-login.readthedocs.io/en/latest/
##      or 
##      https://www.cnblogs.com/agmcs/p/4445428.html

class User:
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


class TodoList:
	# rets: a json string of todolist
	def get_resp():
		pass # TODO: implement this function
	
class Validity:
	# args: valid
	def __init__(valid = False):
		self._valid = valid
	
	# rets: a json string of validity
	def get_resp():
		return Response(json.dumps({'valid': self._valid}), content_type='application/json')
		