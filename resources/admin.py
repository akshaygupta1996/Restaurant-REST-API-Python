from flask_restful import Resource, reqparse
from flask import request, jsonify,make_response
from models.admin import AdminModel
from flask_restful_swagger import swagger
from db import db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

class LoginAdmin(Resource):


		def get(self, username, password, fcmtoken):

				admin = AdminModel.find_by_username(username)
				if admin:
					if admin.password == password:
						# return user_email.json()
						admin.fcmtoken = fcmtoken
						try:
							admin.save_to_db()
						except:
							return {'data':{"status": False}}
						ret = {'data':{'status': True,'admin':{'access_token': create_access_token(identity=admin.id),
								 'fcmtoken': admin.fcmtoken,
								 'priviledges': admin.priviledges}}}
   					  	return make_response(jsonify(ret), 200)
		
				return {'status': False}, 200


