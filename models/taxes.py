# from db import db
from models import db
import datetime
from flask_restful_swagger import swagger


@swagger.model
class TaxesModel(db.Model):

	__tablename__ = "taxes"

	id = db.Column(db.Integer, primary_key = True)
	tax_name = db.Column(db.String(15), nullable = False)
	tax_per = db.Column(db.Float, nullable = False)


	def __init__(self,tax_name, tax_per):

		self.tax_name = tax_name
		self.tax_per = tax_per

	def json(self):
		return {'id': self.id, 'tax_name': self.tax_name, 'tax_per': self.tax_per}


	@classmethod
	def find_by_id(cls, id):
		return cls.query.filter_by(id = id).first()


	def save_to_db(self):

		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()