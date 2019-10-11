from flask_restful import Resource, reqparse
from flask import request, jsonify,make_response
from models.users import UsersModel
from models.userpromo import UserPromoModel
from flask_restful_swagger import swagger
from pyfcm import FCMNotification
from db import db
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import pyrebase

config = {
  "apiKey": "AIzaSyAkC3R1awnMDNSfSbYwFvOPkgO5mtnT1Dg",
  "authDomain": "kmnorth-39c42.firebaseapp.com",
  "databaseURL": "https://kmnorth-39c42.firebaseio.com",
  "storageBucket": "gs://kmnorth-39c42.appspot.com"
}



class NotificationConfirmOrder(Resource):


	def get(self, user_id, order_id):

		user = UsersModel.find_by_id(user_id)
		if user:

			fcmtoken = user.fcmtoken
			fname = user.fname
			lname = user.lname
			firebase = pyrebase.initialize_app(config)
			dbfirebase = firebase.database()
			# k = dbfirebase.child("orders").child(order_id).child().get()
			dbfirebase.child("orders").child(order_id).update({'status': '1'})
			push_service = FCMNotification(api_key="AAAABnCMzP4:APA91bHf4jst14Er5BrZMC9fOVVRGtMUVkPF7VYUI8t3BWbReJJbH_KYui8TIjITnTGZTq8HoKRPztnBsSXAD07m-JA1Tv1Wf6-I4P8gy3coaeMzJpG2K2alBF9iOHJQjbtQhjXuxzFo")
			message_title = "Order Confirmed"
			message_body = "Hey  "+ fname + " " + lname + ". Your Order has been confirmed. You can now track your order"
			push_service.notify_single_device(registration_id=fcmtoken, message_title=message_title, message_body=message_body)
 				
 			return {'data': {'status': True}}

 		else:

 			return {'data': {'status': False}}


class NotificationKitchen(Resource):


	def get(self, user_id, order_id):

		user = UsersModel.find_by_id(user_id)
		if user:

			fcmtoken = user.fcmtoken
			fname = user.fname
			lname = user.lname
			firebase = pyrebase.initialize_app(config)
			dbfirebase = firebase.database()
			dbfirebase.child("orders").child(order_id).update({'status': '2'})
			push_service = FCMNotification(api_key="AAAABnCMzP4:APA91bHf4jst14Er5BrZMC9fOVVRGtMUVkPF7VYUI8t3BWbReJJbH_KYui8TIjITnTGZTq8HoKRPztnBsSXAD07m-JA1Tv1Wf6-I4P8gy3coaeMzJpG2K2alBF9iOHJQjbtQhjXuxzFo")
			message_title = "Your order is in Kitchen"
			message_body = "Hey  "+ fname + " " + lname + ". Your Order is in kitchen....."
			push_service.notify_single_device(registration_id=fcmtoken, message_title=message_title, message_body=message_body)
 				
 			return {'data': {'status': True}}

 		else:

 			return {'data': {'status': False}}

class NotificationOutForDelivery(Resource):


	def get(self, user_id, order_id):

		user = UsersModel.find_by_id(user_id)
		if user:

			fcmtoken = user.fcmtoken
			fname = user.fname
			lname = user.lname
			firebase = pyrebase.initialize_app(config)
			dbfirebase = firebase.database()
			dbfirebase.child("orders").child(order_id).update({'status': '3'})
			push_service = FCMNotification(api_key="AAAABnCMzP4:APA91bHf4jst14Er5BrZMC9fOVVRGtMUVkPF7VYUI8t3BWbReJJbH_KYui8TIjITnTGZTq8HoKRPztnBsSXAD07m-JA1Tv1Wf6-I4P8gy3coaeMzJpG2K2alBF9iOHJQjbtQhjXuxzFo")
			message_title = fname + " " + lname
			message_body = " Your Order is out for delivery.. You can track the delivery boy..."
			push_service.notify_single_device(registration_id=fcmtoken, message_title=message_title, message_body=message_body)
 				
 			return {'data': {'status': True}}

 		else:

 			return {'data': {'status': False}}





