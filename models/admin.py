# from db import db
from models import db
import datetime
import random
from flask_restful_swagger import swagger

@swagger.model
class AdminModel(db.Model):

	__tablename__ = 'admin'

	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(20), nullable = False)
	password = db.Column(db.String(20), nullable = False)
	priviledges = db.Column(db.String(3), nullable = False)
	fcmtoken = db.Column(db.String(300), nullable = False)

	def json(self):
		return { 'id': self.id, 'username': self.username, 'priviledges': self.priviledges}

	@classmethod
	def find_by_username(cls, email):
		return cls.query.filter_by(username = email).first()

	def save_to_db(self):

		db.session.add(self)
		db.session.commit()

