# from db import db
from models import db
import datetime
from flask_restful_swagger import swagger

@swagger.model
class MenuCategoryModel(db.Model):

	__tablename__ = 'menucat'

	id = db.Column(db.Integer, primary_key = True)
	cat_name = db.Column(db.String(50), nullable=False)
	main_cat_id = db.Column(db.Integer, db.ForeignKey('menumaincat.id'))
	menu_items = db.relationship('MenuItemModel', lazy = 'dynamic')
	maincategory = db.relationship('MenuMainCategoryModel')

	def __init__(self, main_cat_id, cat_name):
		self.cat_name = cat_name
		self.main_cat_id = main_cat_id


	def __json__(self):
		json_exclude = getattr(self, '__json_exclude__', set())
		return {key: value for key, value in self.__dict__.items()
				if not key.startswith('_')
				and key not in json_exclude}


	def json(self):
		return { 'id': self.id, 'cat_name': self.cat_name, 'main_cat_id':self.main_cat_id}

	def save_to_db(self):

		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()

	@classmethod
	def find_by_id(cls, cat_id):

		return cls.query.filter_by(id = cat_id).first()