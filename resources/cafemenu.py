from flask_restful import Resource, reqparse
from flask import request
from models.cafemenu import CafeMenuOrder
from models.cafemenuitems import CafeMenuItemsModel
from models.admin import AdminModel
from models.menuitem import MenuItemModel
from flask_restful_swagger import swagger
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

class CafeMenuResorce(Resource):

	parser = reqparse.RequestParser()

	parser.add_argument('payment',
			type = bool,
			required = True,
			help = "Payment Done Not Done")
	parser.add_argument('subtotal',
			type=int,
			required = True,
			help = "Total Amount Required")
	parser.add_argument('tax',
			type = float,
			required = True,
			help = "Amount Tax Required")
	parser.add_argument('total',
			type = float,
			required = True,
			help = "Total Amount Required")
	parser.add_argument('menu',
			type = str,
			required = True,
			help = "menu Array Required")


	def post(self):

		# db.session.begin(subtransactions=True)

		try:

				data = CafeMenuResorce.parser.parse_args()

				order_id = CafeMenuOrder.getOrderNumber()

				print data['menu']




				order = CafeMenuOrder(order_id, data['payment'], data['subtotal'], data['tax'], data['total'])
				try:
					# order.save_to_db()
					# print "Try Block"
					db.session.add(order)
					db.session.flush()
					# order.save_to_db()
					# db.session.commit()
				except:
					return {'data':{"status": False, "message": "Order Failed"}}, 500


				o_id = order.id
				print o_id

				menu = json.loads(data['menu'])
				print menu
				print len(menu)

				for m in menu:

					print m
					print "Order Id"+str(o_id)
					print "Menu Id"+str(m["menu_id"])
					print "Menu Qty"+str(m["menu_qty"])
					print "Menu Amount"+str(m["menu_amount"])
					print "Choice" + str(m["menu_choice"])
					# m = json.loads(me)

					mmodel = CafeMenuItemsModel(o_id, m['menu_id'], m['menu_qty'],m['menu_amount'], m['menu_choice'])

					try:
						# mmodel.save_to_db()
						#print "Menu Try Block"
						# mmodel.save_to_db()
						db.session.add(mmodel)
						# print "Added"
						db.session.flush()
						# print "Flush"
						# db.session.commit()
					except:
						return {'data':{"status": False, "message": "Menu Item Save Failed"}}, 500

					print "Menu Second"

				db.session.commit()
				push_service = FCMNotification(api_key="AAAABnCMzP4:APA91bHf4jst14Er5BrZMC9fOVVRGtMUVkPF7VYUI8t3BWbReJJbH_KYui8TIjITnTGZTq8HoKRPztnBsSXAD07m-JA1Tv1Wf6-I4P8gy3coaeMzJpG2K2alBF9iOHJQjbtQhjXuxzFo")
 
				# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging
				firebase = pyrebase.initialize_app(config)
				dbfirebase = firebase.database()
				data = {"order": order.json(), "menu": menu, "datetime": str(datetime.datetime.now(pytz.timezone('Asia/Calcutta')))}
				dbfirebase.child("cafeorders").child(str(order_id)).set(data)
				admin = AdminModel.find_by_username("admin")
				print admin.fcmtoken
				registration_id = admin.fcmtoken
				message_title = "New Order"
				message_body = "A new Cafe Food order has arrived..!! Confirm the order "
				push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
 
				return {'data': {"status": True, "order": order.json() ,"menu": menu}}
		# except:
		# 	db.session.rollback()
		finally:
			db.session.close()



class CafePaymentDone(Resource):


	def put(self, order_id):

			order = CafeMenuOrder.find_by_code(order_id)
			if order:
				order.payment = True
				order.save_to_db()

				firebase = pyrebase.initialize_app(config)
				dbfirebase = firebase.database()
			# k = dbfirebase.child("orders").child(order_id).child().get()
				dbfirebase.child("cafeorders").child(order.order_id).child("order").update({'payment': '1'})

				return {"data": {"status": True}}

			return {"data": {"status": False}}


class CafeItemsTest(Resource):


	def post(self):

		mmodel = CafeMenuItemsModel(33,4,1,50,0)
		mmodel.save_to_db()



class CafeBookingPaymentConfirmed(Resource):



	def put(self, order_id):

		order = CafeMenuOrder.find_by_id(order_id)
		if order:
			order.payment = True
			order.save_to_db()
			firebase = pyrebase.initialize_app(config)
			dbfirebase = firebase.database()
			# k = dbfirebase.child("orders").child(order_id).child().get()
			dbfirebase.child("cafeorders").child(order.order_id).child("order").update({'payment': True})


			return {"data": {"status": True}}
		else:
			return {"data": {"status": False}}


class CafeOrders(Resource):

	def get(self, date):


		result = db.session.execute("Select * from cafemenu where cast(date_time as date) = '"+date+"';");

		orders = []
		menu = []

		for r in result:
			o = dict()
			o['id'] = r['id']
			o['order_id'] = str(r['order_id'])
			o['payment'] = r['payment']
			o['subtotal'] = r['subtotal']
			o['tax'] = r['tax']
			o['total'] = r['total']
			o['date_time'] = str(r['date_time'])
			orders.append(o)
			menuitems = CafeMenuItemsModel.query.filter_by(order_no = r['id']).all()
			items = []
			for m in menuitems:
				menuitem = MenuItemModel.query.filter_by(id = m.menu_item_id).first()

				item = {'menu_id': m.id, 'menu_qty': m.menu_qty, 'menu_amount': m.menu_amount, 'menu_choice': m.choice, 'menu_name': menuitem.name, 'menu_choice_one': menuitem.choice_one, 'menu_choice_two': menuitem.choice_two, 'menu_description': menuitem.description}
				items.append(item)
			menu.append(items)


		fuck_all_order = [{"order": o, "menu": m} for o,m in zip(orders, menu)]
		return {'data':{'status': True, 'menu': fuck_all_order}}










