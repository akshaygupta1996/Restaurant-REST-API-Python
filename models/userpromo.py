# from db import db
from models import db
from flask_restful_swagger import swagger


class UserPromoModel(db.Model):

	__tablename__ = "userpromo"

	userpromo_id = db.Column(db.Integer, primary_key = True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	promo_code = db.Column(db.String(8), db.ForeignKey('promocode.promo_code'))
	userpromo_validity = db.Column(db.Date, nullable = False)
	userpromo_used = db.Column(db.Boolean, default = False, nullable = False)
	user = db.relationship('UsersModel')
	promo = db.relationship('PromoCodeModel')


	def __init__(self, user_id, promo_code,userpromo_validity, userpromo_used):
		self.user_id = user_id
		self.promo_code = promo_code
		self.userpromo_used  = userpromo_used
		self.userpromo_validity = userpromo_validity

	def json(self):
		return {'userpromo_id': self.userpromo_id,'promo_code':self.promo_code ,'user_id': self.user_id, 'userpromo_used': self.userpromo_used, 'userpromo_validity': str(self.userpromo_validity)}

	@classmethod
	def find_by_id(cls,userpromo_id):
		return cls.query.filter_by(userpromo_id = userpromo_id).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()
