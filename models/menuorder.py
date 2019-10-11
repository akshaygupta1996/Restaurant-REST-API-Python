# from db import db
from models import db
import datetime
import random
from flask_restful_swagger import swagger
import pytz

class MenuOrderModel(db.Model):

	__tablename__ = "menuorder"

	id = db.Column(db.Integer, primary_key = True)
	order_id = db.Column(db.Integer)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	payment_id = db.Column(db.Integer, db.ForeignKey('payment.id'))
	address_id = db.Column(db.Integer, db.ForeignKey('users_address.id'))
	promo_code = db.Column(db.String(10), nullable = True)
	date_time = db.Column(db.DateTime, default =datetime.datetime.now(pytz.timezone('Asia/Calcutta')))
	special_note = db.Column(db.String(100), nullable = True)
	ratings = db.Column(db.Integer, nullable = True)
	approved = db.Column(db.Boolean, nullable = False)
	users = db.relationship('UsersModel')
	payment = db.relationship('PaymentModel')
	address = db.relationship('UsersAddressModel')
	menuorderitem = db.relationship('MenuOrderItemModel', lazy = 'dynamic')



	def __init__(self,order_id, user_id, payment_id, address_id, promo_code, special_note, ratings, approved):

		self.order_id = order_id
		self.user_id = user_id
		self.payment_id = payment_id
		self.address_id = address_id 
		self.promo_code = promo_code
		self.special_note = special_note
		self.ratings = ratings
		self.approved = approved


	def json(self):
		return {'order_id': self.order_id, 'user_id': self.user_id, 'payment_id': self.payment_id, 'address_id': self.address_id, 'promo_code': self.promo_code, 'special_note': self.special_note, 'ratings': self.ratings, 'approved': self.approved}

	@classmethod
	def find_by_id(cls, id):
		return cls.query.filter_by(id = id).first()


	@classmethod
	def find_by_code(cls, code):
		return cls.query.filter_by(order_id = code).first()


	@classmethod
	def getOrderNumber(cls):

		now = datetime.datetime.now(pytz.timezone('Asia/Calcutta'))
		d= now.day
		m = now.month
		y = now.year
		date = str(y)+'-'+str(m)+'-'+str(d)
		print date
		result = db.session.execute("SELECT MAX(order_id) + 1 as ord from menuorder where cast(date_time as Date) ='"+date+"';")
		for r in result:
			if r['ord'] is None:
				return 1
			else:
				return int(r['ord'])
		# ref = str(random.randint(100000, 999999))

		# order = MenuOrderModel.find_by_code(ref)
		# if order is None:
		# 	return ref
		# else:
		# 	getOrderNumber()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

