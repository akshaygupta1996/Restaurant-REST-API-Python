# from db import db
from models import db
import datetime
import random
from flask_restful_swagger import swagger
import pytz

class PaymentModel(db.Model):

	__tablename__ = "payment"

	id = db.Column(db.Integer, primary_key = True)
	payment_type = db.Column(db.String(2), nullable = False)
	transaction_id = db.Column(db.String(12), unique = True, nullable = False)
	date_time_of_payment = db.Column(db.DateTime, default =datetime.datetime.now(pytz.timezone('Asia/Calcutta')))
	amount = db.Column(db.Integer, nullable = False)
	amount_payable = db.Column(db.Integer, nullable = False)
	amount_tax = db.Column(db.Integer, nullable = False)
	amount_menu = db.Column(db.Integer, nullable = False)
	amount_discount = db.Column(db.Integer, nullable = False)
	amount_wallet = db.Column(db.Integer, nullable = False)
	menuorder = db.relationship('MenuOrderModel', lazy = 'dynamic')
	# users = db.relationship('UsersModel', lazy = 'dynamic')

	def __init__(self,payment_type, transaction_id, amount, amount_payable, amount_tax, amount_menu, amount_discount, amount_wallet):
		self.payment_type = payment_type
		self.transaction_id = transaction_id
		self.amount = amount
		self.amount_payable = amount_payable
		self.amount_menu = amount_menu
		self.amount_wallet = amount_wallet
		self.amount_tax = amount_tax
		self.amount_discount = amount_discount


	def json(self):
		return {'id': self.id, 'payment_type': self.payment_type, 'transaction_id': self.transaction_id, 'date_time_of_payment': str(self.date_time_of_payment),'amount': self.amount, 'amount_discount': self.amount_discount, 'amount_tax': self.amount_tax, 'amount_wallet': self.amount_wallet, 'amount_menu': self.amount_menu, 'amount_payable': self.amount_payable}


	@classmethod
	def find_by_id(cls, id):
		return cls.query.filter_by(id = id).first()


	def save_to_db(self):
		db.session.add(self)
		db.session.commit()