from flask_restful import Resource, reqparse
from flask import request
from models.promocode import PromoCodeModel
from flask_restful_swagger import swagger
from datetime import datetime

class PromoCode(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('promo_code',
			type = str,
			required = True,
			help = "Promo Code is Required"
			)
	parser.add_argument('promo_discount_per',
			type = int,
			required = True,
			help = "Promo Code Discount Percentage is Required"
			)
	parser.add_argument('promo_validity',
			type = str,
			required = True,
			help = "Promo  Validity is Required. Format: YYYY-MM-DD"
			)
	parser.add_argument('promo_wallet',
		type = bool,
		required = True,
		help = "Cashback on wallet or Discount on Order ?? ")
	parser.add_argument('promo_user', 
		type=bool,
		required = True,
		help = "Promo Code Valid For all Users Or Not")
	parser.add_argument('promo_description',
		type = str,
		required = True,
		help = "Promo Code Description")
	parser.add_argument('promo_url',
		type = str,
		required = False)

	@swagger.operation(
		notes='Adding A Promo Code',
		nickname='POST',
		parameters=[
			{
				"name": "promo_code",
				"required": True,
				"dataType": "string"
			},
			{
				"name": "promo_discount_per",
				"required": True,
				"dataType":"int"
			},
			{
				"name": "promo_validity",
				"required": True,
				"dataType": "Date"
			},
			{
				"name":"promo_wallet",
				"required": True,
				"dataType": "Boolean"
			},
			{
				"name": "promo_user",
				"required": True,
				"dataType": "Boolean"
			},
			{
				"name": "promo_description",
				"required": True,
				"dataType": "String"
			},
			{
				"name": "promo_url",
				"required": False,
				"dataType": "String"
			}]
		)
	def post(self):
		data = PromoCode.parser.parse_args()
		datetime_object = datetime.strptime(data['promo_validity'],'%Y-%m-%d')
		if data['promo_url'] is None:
			promocode = PromoCodeModel(data['promo_code'], data['promo_discount_per'], datetime_object, data["promo_wallet"], data["promo_user"], data["promo_description"],None)
		else:
			promocode = PromoCodeModel(data['promo_code'], data['promo_discount_per'], datetime_object, data["promo_wallet"], data["promo_user"], data["promo_description"],data["promo_url"])
		try:
			promocode.save_to_db()
		except:
			return {'data':{"status": False}}, 500
		
		return {'data':{'status': True, 'promocode': promocode.json()}}, 201

	@swagger.operation(
		notes='Get List of all Promo Code',
		nickname='GET'
		)

	def get(self):

		return {'data':{'promocode': [promo.json() for promo in PromoCodeModel.query.all()]}}

class PromoCodeEdit(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('promo_validity',
			type = str,
			required = True,
			help = "Promo Code Validity is Required..  Format: YYYY-MM-DD"
			)
	parser.add_argument('promo_description',
			type = str,
			required = True,
			help = " Promo Code Desciption")

	@swagger.operation(
		notes='Edit a Promo Code Validity',
		nickname='PUT',
		parameters=[
			{
				"name": "promo_id",
				"required": True,
				"dataType": "int"
			},
			{
				"name": "promo_validity",
				"required": True,
				"dataType": "Date"
			},
			{
				"name": "promo_description",
				"required": True,
				"dataType": "String"
			}]
		)

	def put(self, promo_id):

		promocode = PromoCodeModel.find_by_promo_id(promo_id)
		data = PromoCodeEdit.parser.parse_args()
		if promocode:
			promocode.promo_validity = data['promo_validity']
			promocode.promo_description = data['desciption']
			promocode.save_to_db()
			return {'data':{'status': True, 'promocode': promocode.json()}}

		return {'data': {'status': False}}

	# @swagger.operation(
	# 	notes='Delete a Promo Code',
	# 	nickname='DELETE',
	# 	parameters=[
	# 		{
	# 			"name": "promo_id",
	# 			"required": True,
	# 			"dataType": "int"
	# 		}]
	# 	)

	# def delete(self, promo_id):

	# 	promocode = PromoCodeModel.find_by_promo_id(promo_id)
	# 	if promocode:
	# 		promocode.delete_from_db()
	# 		return {'data': {'status': True}}
	# 	return {'data': {'status': False}}

class PromoCodeForAll(Resource):


	@swagger.operation(
		notes = "List All Promo Codes Valid For All Users",
		nickname = 'GET')

	def get(self):
		date = datetime.now().date()

		return {'data':{'promocode': [promo.json() for promo in PromoCodeModel.query.filter(PromoCodeModel.promo_validity >= date, PromoCodeModel.promo_user == 0)]}}





 

