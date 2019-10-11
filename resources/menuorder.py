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

config = {
  "apiKey": "AIzaSyAkC3R1awnMDNSfSbYwFvOPkgO5mtnT1Dg",
  "authDomain": "kmnorth-39c42.firebaseapp.com",
  "databaseURL": "https://kmnorth-39c42.firebaseio.com",
  "storageBucket": "gs://kmnorth-39c42.appspot.com"
}


class MenuOrderResource(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('user_id',
			type = int,
			required = True,
			help = "User Id is required"
		)
	parser.add_argument('address_id',
			type = int,
			required = True,
			help = "Address Required")
	parser.add_argument('promo_code',
			type=str,
			required = True,
			help = "Promo Code Required")
	parser.add_argument('special_note_required',
			type = str,
			required = True,
			help = "Sepcial Note Required")
	parser.add_argument('payment_type',
			type = str,
			required = True,
			help = "Payment Type CD/OP")
	parser.add_argument('amount',
			type = int,
			required = True,
			help = "Amount Required")
	parser.add_argument('amount_payable',
			type=int,
			required = True,
			help = "Amount Payable Required")
	parser.add_argument('amount_tax',
			type = int,
			required = True,
			help = "Amount Tax Required")
	parser.add_argument('amount_discount',
			type = int,
			required = True,
			help = "Amount Discount Required")
	parser.add_argument('amount_wallet',
			type = int,
			required = True,
			help = "Amount Wallet Required")
	parser.add_argument('amount_menu',
			type = int,
			required = True,
			help = "Amount Menu Required")
	parser.add_argument('menu',
			type = str,
			required = True,
			help = "menu Array Required")
	parser.add_argument('ratings',
			type = int,
			required = False)


	def post(self):

		# db.session.begin(subtransactions=True)

		try:

			data = MenuOrderResource.parser.parse_args()

			if data['payment_type'] == "CD":
				payment = PaymentModel(data['payment_type'], "COD", data['amount'], data['amount_payable'], data['amount_tax'], data['amount_menu'], data['amount_discount'], data['amount_wallet'] )
				try:
					# payment.save_to_db()
					db.session.add(payment)
					db.session.flush()
					# db.session.commit()
				except:
					return {'data':{"status": False, "message": "Paymnet False"}}, 500

				

				# payment_id = payment.id

				order_id = MenuOrderModel.getOrderNumber()

				order = MenuOrderModel(order_id, data['user_id'],payment.id, data['address_id'],data['promo_code'],data['special_note_required'],data['ratings'],0)
				try:
					# order.save_to_db()
					db.session.add(order)
					db.session.flush()
					# db.session.commit()
				except:
					return {'data':{"status": False, "message": "Order Failed"}}, 500


				o_id = order.id

				menu = json.loads(data['menu'])

				for m in menu:

					print str(m)
					# m = json.loads(me)

					mmodel = MenuOrderItemModel(o_id, m['menu_id'], m['menu_qty'],m['menu_amount'], m['menu_choice'])

					try:
						# mmodel.save_to_db()
						db.session.add(mmodel)
						db.session.flush()
						# db.session.commit()
					except:
						return {'data':{"status": False, "message": "Menu Item Save Failed"}}, 500

				db.session.commit()
				push_service = FCMNotification(api_key="AAAABnCMzP4:APA91bHf4jst14Er5BrZMC9fOVVRGtMUVkPF7VYUI8t3BWbReJJbH_KYui8TIjITnTGZTq8HoKRPztnBsSXAD07m-JA1Tv1Wf6-I4P8gy3coaeMzJpG2K2alBF9iOHJQjbtQhjXuxzFo")
 
				# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging
				firebase = pyrebase.initialize_app(config)
				dbfirebase = firebase.database()

				user = UsersModel.find_by_id(int(data['user_id']))
				address = UsersAddressModel.find_by_id(int(data['address_id']))
				data = {"user_id": data['user_id'], "status": "0", "order": order.json(), "payment": payment.json(), "menu": menu, "user": user.json(), "address": address.json(), "datetime": str(datetime.datetime.now(pytz.timezone('Asia/Calcutta')))}
				dbfirebase.child("orders").child(str(order_id)).set(data)
				admin = AdminModel.find_by_username("admin")
				print admin.fcmtoken
				registration_id = admin.fcmtoken
				message_title = "New Order"
				message_body = "A new Food order has arrived..!! Confirm the order "
				push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
 
				return {'data': {"status": True, "payment": payment.json(), "order": order.json() ,"menu": menu}}
		# except:
		# 	db.session.rollback()
		finally:
			db.session.close()





class MenuOrderResourceEdit(Resource):

 

	def put(self, order_id):

		order = MenuOrderModel.find_by_code(order_id)
		if order:
			order.approved = True
			order.save_to_db()

			return {"data": {"status": True}}

		return {"data": {"status": False}}


class MenuOrderResourceEditRatings(Resource):



	def put(self, order_id, ratings):

		order = MenuOrderModel.find_by_code(order_id)
		if order:
			order.ratings = ratings
			order.save_to_db()

			return {"data": {"status": True}}

		return {"data": {"status": False}}

class MenuOrderForUsers(Resource):


	def get(self, user_id):

		orders = MenuOrderModel.query.filter_by(user_id = user_id).order_by(desc(MenuOrderModel.date_time)).all()

		menuorder = []
		payment = []
		menu = []
		for order in orders:
			menuorder.append(order.json())
			p = PaymentModel.query.filter_by(id = order.payment_id).first()
			payment.append(p.json())

			menuitems = MenuOrderItemModel.query.filter_by(order_no = order.id).all()
			items = []
			for m in menuitems:
				menuitem = MenuItemModel.query.filter_by(id = m.menu_item_id).first()

				item = {'menu_id': m.id, 'menu_qty': m.menu_qty, 'menu_amount': m.menu_amount, 'menu_choice': m.choice, 'menu_name': menuitem.name, 'menu_choice_one': menuitem.choice_one, 'menu_choice_two': menuitem.choice_two, 'menu_description': menuitem.description}
				items.append(item)
			menu.append(items)

		fuck_all_order = [{"status": True, "payment": p, "order": o, "menu": m} for p,o,m in zip(payment, menuorder, menu)]
		return {'data':{'status': True, 'menu': fuck_all_order}}



class TestOrderId(Resource):


	def get(self):

		order_id = MenuOrderModel.getOrderNumber()

		return {'data': order_id}


	