# from db import db
# from db import db
from models import db
from flask_restful_swagger import swagger


class MenuItemModel(db.Model):

	__tablename__ = 'menuitem'

	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(30), nullable = False)
	description = db.Column(db.String(150))
	full_price = db.Column(db.Integer, nullable = False)
	half_price = db.Column(db.Integer, nullable = True)
	choice = db.Column(db.Boolean, default = False)
	choice_one = db.Column(db.String(80), nullable = True)
	choice_two = db.Column(db.String(80), nullable = True)
	# image_path = db.Column(db.String(400))
	cat_id = db.Column(db.Integer, db.ForeignKey('menucat.id'))
	category = db.relationship('MenuCategoryModel')

	def __init__(self, name, description, full_price, half_price, cat_id, choice, choice_one, choice_two):
		self.name = name
		self.description = description
		self.full_price = full_price
		self.half_price = half_price
		self.cat_id = cat_id
		self.choice = choice
		self.choice_one = choice_one
		self.choice_two = choice_two

	def __json__(self):
		json_exclude = getattr(self, '__json_exclude__', set())
		return {key: value for key, value in self.__dict__.items()
				if not key.startswith('_')
				and key not in json_exclude}


		# self.image_path = image_path



	def json(self):
		return {'id': self.id, 'name': self.name, 'description': self.description, 'full_price': self.full_price, 'half_price': self.half_price, 'cat_id': self.cat_id, 'choice':self.choice, 'choice_one': self.choice_one, 'choice_two': self.choice_two}


	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

	@classmethod
	def find_by_id(cls, menu_id):

		return cls.query.filter_by(id = menu_id).first()

