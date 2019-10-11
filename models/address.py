# from db import db
from models import db
import datetime
from flask_restful_swagger import swagger


@swagger.model
class UsersAddressModel(db.Model):

	__tablename__ = 'users_address'

	id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	delivery_area = db.Column(db.String(50))
	address = db.Column(db.String(150))
	instructions = db.Column(db.String(150))
	user = db.relationship('UsersModel')


	def __init__(self,user_id, delivery_area, address, instructions):
		self.user_id = user_id
		self.delivery_area = delivery_area
		self.address = address
		self.instructions = instructions


	def json(self):
		return {'id': self.id, 'user_id': self.user_id, 'delivery_area': self.delivery_area, 'instructions': self.instructions, 'address': self.address }



	@classmethod
	def find_by_id(cls, address_id):

		return cls.query.filter_by(id = address_id).first()

	def save_to_db(self):

		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()


