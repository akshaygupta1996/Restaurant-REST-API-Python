# from db import db
from models import db
from flask_restful_swagger import swagger


@swagger.model
class PromoCodeModel(db.Model):

	__tablename__ = "promocode"

	promo_id = db.Column(db.Integer, primary_key = True)
	promo_code = db.Column(db.String(10), nullable = False, unique = True)
	promo_discount_per = db.Column(db.Integer, nullable = False)
	promo_validity = db.Column(db.Date, nullable = False)
	promo_wallet = db.Column(db.Boolean, nullable = False)   # True=> Cashback On Wallet   False=> Discount on Total Amount
	promo_user = db.Column(db.Boolean, nullable = False)	 # True=>Not For all Users     False=> For All Users
	promo_description = db.Column(db.String(100), nullable = False)
	promo_url = db.Column(db.String(100), nullable = False)
	promouser = db.relationship('UserPromoModel' , lazy = 'dynamic')
	# users = db.relationship('MenuOrderModel', lazy = 'dynamic')
	


	def __init__(self, promo_code, promo_discount_per, promo_validity, promo_wallet, promo_user, promo_description, promo_url):
		self.promo_code = promo_code
		self.promo_discount_per = promo_discount_per
		self.promo_validity = promo_validity
		self.promo_wallet = promo_wallet
		self.promo_user = promo_user
		self.promo_description = promo_description
		self.promo_url = promo_url


	def json(self):
		return {'promo_id':self.promo_id, "promo_code": self.promo_code, "promo_validity": str(self.promo_validity), "promo_discount_per": self.promo_discount_per, "promo_wallet": self.promo_wallet, "promo_user": self.promo_user, "promo_description": self.promo_description, "promo_url": self.promo_url}

	@classmethod
	def find_by_promo_code(cls, promo_code):
		return cls.query.filter_by(promo_code = promo_code).first()

	@classmethod
	def find_by_promo_id(cls, promo_id):
		return cls.query.filter_by(promo_id = promo_id).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete_from_db(self):
		db.session.delete(self)
		db.session.commit()
