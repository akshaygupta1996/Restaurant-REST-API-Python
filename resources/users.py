from flask_restful import Resource, reqparse
from flask import request, jsonify,make_response
from models.users import UsersModel
from models.userpromo import UserPromoModel
from flask_restful_swagger import swagger
from db import db

import requests
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

import firebase_admin
from firebase_admin import auth
class Users(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('fname',
			type = str,
			required = True,
			help = "First Name is Required"
			)
	parser.add_argument('lname',
			type = str,
			required = True,
			help = "Last Name is Required")
	parser.add_argument('phone_number',
			type = str,
			required = True,
			help = "Phone Number Required")
	parser.add_argument('email',
			type = str,
			required = True,
			help = "Email Required")
	parser.add_argument('password',
		type = str,
		required = True,
		help = "Password Required")
	parser.add_argument('register_ref',
		type=str,
		required = True,
		help = "If Users does not provide Ref Code then pass 0")
	@swagger.operation(
		notes = "Get All Registered Users",
		nickname='GET')

	def get(self):

		return {'users': [user.json() for user in UsersModel.query.all()]}

	
	@swagger.operation(
		notes='Register a User',
		nickname='POST',
		parameters=[
			{
				"name": "fname",
				"required": True,
				"dataType": "String"
			},
			{
				"name": "lname",
				"required": True,
				"dataType": "String"
			},
			{
				"name": "email",
				"required": True,
				"dataType": "String"
			},
			{
				"name": "phone_number",
				"required": True,
				"dataType": "String"
			},
			{
				"name": "password",
				"required": True,
				"dataType": "String"
			},
			{
				"name": "register_ref",
				"required": True,
				"dataType": "String"
			}

		])
	def post(self):


		data = Users.parser.parse_args()

		if UsersModel.find_by_email(data['email']):
			return {'data':{'status': False,
							'message': "Email Already Regsitered"}}, 201

		if UsersModel.find_by_phone(data['phone_number']):
			return {'data':{'status': False,
							'message': "Phone Number Already Registered"}}, 201
			# return {'error': "Phone Number Already Registered"}, 400

		if data['register_ref'] == "0":
			
			refcode = UsersModel.getRefCode(data['fname'])
			user = UsersModel(data['fname'], data['lname'], data['email'], data['phone_number'], data['password'],refcode, data['register_ref'],0,"fcm")
			try:
				user.save_to_db()
			except:
				return {'message': "An Error Occured"}, 500

			return {'data':{'status': True, 'message': "Registration Successful"}}, 201


		else:
			user_ref =  UsersModel.find_by_refcode(data['register_ref'])
			if user_ref is not None:
				no = user_ref.register_ref_no
				if no == 2:
					return {'data': {'status': False,
								'message': "User Crossed his/her Limit"}}
					#refernece code cannot be added. User crosseds the limit

				elif no < 2:
					no = no + 1
					user_ref.register_ref_no = no

					try:
						db.session.commit()
					except:
						return {'message': "An Error Occured"}, 500

					userpromo = UserPromoModel(user_ref.id, "REF020", "2018-12-12", False)
					
					try:
						userpromo.save_to_db()
					except:
						return {'message': "User promo table Error"}, 500
					refcode = UsersModel.getRefCode(data['fname'])
					user = UsersModel(data['fname'], data['lname'], data['email'], data['phone_number'], data['password'],refcode, data['register_ref'],0,"fcm")

					try:
						user.save_to_db()
						user_id_for_promo = user.id
						userpromo_u = UserPromoModel(user_id_for_promo, "REF010", "2018-12-12", False)
						userpromo_u.save_to_db()
					except:
						return {'message': "An Error Occured"}, 500

					return {'data':{'status': True, 'message': "Registration Successful"}}, 201
			else:
				return {'data': {'status': False,
								'message': "Reference Code Invalid"}}
		

class LoginUsers(Resource):

		@swagger.operation(
			notes='Login User',
			nickname='GET',
			parameters=[
			{
				"name": "flag",
				"required": True,
				"dataType": "INT",
				"description": "0 for Email and 1 for Phone"
			},
			{
				"name": "user_ep",
				"required": True,
				"dataType": "String",
				"description": "If flag 0 then pass email else phone_number"
			},
			{
				"name": "password",
				"required": True,
				"dataType": "String"
			}

		])

		def get(self, flag, user_ep,password, fcmtoken):

			if flag == 0:
				user_email = UsersModel.find_by_email(user_ep)
				if user_email:
					if user_email.password == password:
						user_email.fcmtoken = fcmtoken
						user_email.save_to_db()
						# return user_email.json()
						custom_token = auth.create_custom_token(user_ep)
						ret = {'status': True,'user':{'access_token': create_access_token(identity=user_email.id),
								 'user_id': user_email.id,
								 'custom_token': custom_token,
								 'fname': user_email.fname,
								 'lname': user_email.lname,
								 'email': user_email.email,
								 'refcode': user_email.refcode,
								 'alt_phone_number': user_email.alt_phone_number,
								 'phone_number': user_email.phone_number}}
   					  	return make_response(jsonify(ret), 200)
			if flag == 1:
				user_phone = UsersModel.find_by_phone(user_ep)
				if user_phone:
					if user_phone.password == password:
						user_phone.fcmtoken = fcmtoken
						user_phone.save_to_db()
						# return user_phone.json()
						custom_token = auth.create_custom_token(user_ep)
						ret = {'status': True, 'user':{'access_token': create_access_token(identity=user_phone.id),
								 'user_id': user_phone.id,
								 'custom_token': custom_token,
								 'fname': user_phone.fname,
								 'lname': user_phone.lname,
								 'email': user_phone.email,
								 'refcode': user_phone.refcode,
								 'alt_phone_number': user_phone.alt_phone_number,
								 'phone_number': user_phone.phone_number}}
   					  	return make_response(jsonify(ret), 200)
		
			return {'status': False}, 200


class UserPhoneNumber(Resource):

	def put(self, user_id, alt_phone_number):

		user = UsersModel.find_by_id(user_id)

		if user:
			user.alt_phone_number = alt_phone_number
			user.save_to_db()
			return {'data':{'status': True, 'user': user.json()}}

		else:
			return {"data": {"status": False}}



class ForgetPassword(Resource):

	def get(self, phone_number):


		user = UsersModel.find_by_phone(phone_number)
		if user:
			password = user.password
			r = requests.get('http://roundsms.com/api/sendhttp.php?authkey=NGUwNDYxZmNiY2N&mobiles='+str(phone_number)+'&Your password for KM NORTH '+password+'.&sender=KMNORT&type=1&route=2')
			return {"data": {"status": True, "res": r.json()}}
		else:

			return {"data": {"status": False}}

class ChangePassword(Resource):

	def put(self, user_id, password, new_password):

		user = UsersModel.find_by_id(user_id)
		if user is not None:

			if user.password == password:

				user.password = new_password
				try:
					user.save_to_db()
					return {"data":{"status": True}}
				except:
					return {"data": {"status": False}}


		return {"data": {"status": False}}