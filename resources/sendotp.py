from flask_restful import Resource, reqparse
from flask import request
from models.menuorder import MenuOrderModel
from models.menuorderitems import MenuOrderItemModel
from models.payment import PaymentModel
from models.menuitem import MenuItemModel
from models.admin import AdminModel
from models.users import UsersModel
from models.address import UsersAddressModel
from flask_restful_swagger import swagger
from sqlalchemy import desc
from pyfcm import FCMNotification
import json
import datetime
from db import db
from flask import jsonify
import pyrebase
import pytz
import requests
from random import randint



class SendOtpTest(Resource):


	def get(self, phone_number): 

		otp = randint(1000, 9999)
		
		r = requests.get('http://roundsms.com/api/sendhttp.php?authkey=NGUwNDYxZmNiY2N&mobiles='+str(phone_number)+'&message=Welcome to KM North.. Your OTP is '+str(otp)+'.&sender=KMNORT&type=1&route=2')
		
		return {"data": {"res":r.json(), "otp": otp}}



	

