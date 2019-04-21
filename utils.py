# -*- coding: utf-8 -*-

#from models import User


    
class Validity:
	# args: valid
    def __init__(self, valid = False,
                     info = ''):
        self._valid = valid
        self._info = info
	
	# rets: a json string of validity
    def get_resp(self):
        return Response(json.dumps({'valid': self._valid,
									'info': self._info}),
						content_type='application/json')