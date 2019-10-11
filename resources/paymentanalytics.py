from flask_restful import Resource, reqparse
from flask import request
from models.payment import PaymentModel
from flask_restful_swagger import swagger
from pyfcm import FCMNotification
import json
import datetime
from db import db
from flask import jsonify
import pyrebase
import pytz



class DailyPaymentDetails(Resource):




	def get(self, dateone, datetwo):
	

		result = db.session.execute("SELECT SUM(amount_payable) as payable , SUM(amount_tax) as tax, SUM(amount_menu) as menuprice, SUM(amount_discount) as discount, SUM(amount_wallet) as delivery from payment where cast(date_time_of_payment as Date) >= '"+ dateone + "'  and cast(date_time_of_payment as Date) <= '"+ datetwo+"';")

		
		re = dict()
		for r in result:
			re['payable'] = str(r['payable'])
			re['tax'] = str(r['tax'])
			re['menuprice'] = str(r['menuprice'])
			re['discount'] = str(r['discount'])
			re['delivery'] = str(r['delivery'])
			# re.append({'payable': str(r['payable'])})

		return {"data": re}