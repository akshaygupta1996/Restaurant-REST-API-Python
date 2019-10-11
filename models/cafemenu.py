from models import db
import datetime
import random
from flask_restful_swagger import swagger
import pytz


class CafeMenuOrder(db.Model):

	__tablename__ = "cafemenu"

	id = db.Column(db.Integer, primary_key = True)
	order_id = db.Column(db.String(10), nullable = False)
	date_time = db.Column(db.DateTime, default =datetime.datetime.now(pytz.timezone('Asia/Calcutta')))
	payment = db.Column(db.Boolean, nullable = False)
	subtotal = db.Column(db.Integer, nullable = False)
	tax = db.Column(db.Float, nullable = False)
	total = db.Column(db.Float, nullable = False)
	# cafemenuorderitem = db.relationship('CafeMenuItemsModel', lazy = 'dynamic')


	def __init__(self, order_id, payment, subtotal, tax, total):

		self.order_id = order_id
		self.payment = payment
		self.subtotal = subtotal
		self.tax = tax
		self.total = total


	def json(self):
		return {'id': self.id, 'order_id': self.order_id,'date_time': str(self.date_time), 'payment': self.payment, 'subtotal': self.subtotal, 'tax': self.tax, 'total': self.total}

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
		result = db.session.execute("SELECT MAX(CAST(TRIM(leading 'O' FROM order_id) AS unsigned)) + 1 as ord from cafemenu where cast(date_time as Date) ='"+date+"';")
		for r in result:
			if r['ord'] is None:
				return "O1"
			else:
				return "O"+str(int(r['ord']))
		# ref = str(random.randint(100000, 999999))

		# order = MenuOrderModel.find_by_code(ref)
		# if order is None:
		# 	return ref
		# else:
		# 	getOrderNumber()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

