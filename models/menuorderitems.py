# from db import db
from models import db
import datetime
import random
from flask_restful_swagger import swagger

class MenuOrderItemModel(db.Model):

	__tablename__ = "menuorderitems"


	id = db.Column(db.Integer, primary_key = True)
	order_no  =db.Column(db.Integer, db.ForeignKey('menuorder.id'))
	menu_item_id = db.Column(db.Integer, db.ForeignKey('menuitem.id'))
	menu_qty = db.Column(db.Integer, nullable = False)
	menu_amount = db.Column(db.Integer, nullable = False)
	choice = db.Column(db.Integer, nullable = True)
	menuorder = db.relationship('MenuOrderModel')
	menuitem = db.relationship('MenuItemModel')

	def __init__(self,order_no, menu_item_id, menu_qty, menu_amount, choice):
		self.order_no = order_no
		self.menu_item_id = menu_item_id
		self.menu_qty = menu_qty
		self.menu_amount = menu_amount
		self.choice = choice


	def json(self):
		return {'id': self.id, 'order_no': self.order_no, 'menu_item_id': self.menu_item_id, 'menu_qty': self.menu_qty, 'menu_amount': self.menu_amount, 'choice': self.choice}

	@classmethod
	def find_by_id(cls, id):
		return cls.query.filter_by(id = id).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()