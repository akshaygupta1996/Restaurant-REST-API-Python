from flask_restful import Resource, reqparse
from flask import request
from models.taxes import TaxesModel
from flask_restful_swagger import swagger
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


class Tax(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('tax_name',
			type = str,
			required = True,
			help = "Tax Name is Required"
			)
	parser.add_argument('tax_per',
			type = str,
			required = True,
			help = "Tax Percentage is Required")

	@swagger.operation(
		notes='Adding A Tax',
		nickname='POST',
		parameters=[
			{
				"name": "tax_name",
				"required": True,
				"dataType": "string"
			},
			{
				"name": "tax_per",
				"required": True,
				"dataType": "int"
			}
		])
	
	def post(self):

		data = Tax.parser.parse_args()
		tax = TaxesModel(data['tax_name'], data['tax_per'])
		try:
			tax.save_to_db()
		except:
			return {'data':{"status": False}}, 500
		
		return {'data':{'status': True, 'tax': tax.json()}}, 201

	@swagger.operation(
		notes='Getting List of Tax',
		nickname='GET')
	
	def get(self):

		return {'data':{'taxes': [tax.json() for tax in TaxesModel.query.all()]}}

class TaxEdit(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('tax_name',
			type = str,
			required = True,
			help = "Tax Name is Required")
	parser.add_argument('tax_per',
			type=int,
			required = True,
			help = "Tax Percentage is Required")


	@swagger.operation(
		notes='Edit an Tax',
		nickname='PUT',
		parameters=[
			{
				"name": "id",
				"required": True,
				"dataType": "int"
			},
			{ 
				"name": "tax_name",
				"required": True,
				"dataType": "String"
			},
			{
				"name": "tax_per",
				"required": True,
				"dataType": "int"
			}
		])

	def put(self, id):
		tax = TaxesModel.find_by_id(id)
		if tax:
			data = TaxEdit.parser.parse_args()
			tax.tax_name = data['tax_name']
			tax.tax_per = data['tax_per']
			tax.save_to_db()
			return {'data':{'status': True, 'tax': tax.json()}}
		return {'data':{'status': False}}

	@swagger.operation(
		notes='Delete An Tax',
		nickname='DELETE',
		parameters=[
			{
				"name": "id",
				"required": True,
				"dataType": "int"
			}
		])

	def delete(self, id):
		
		data = TaxEdit.parser.parse_args()

		tax = TaxesModel.find_by_id(id)
		if tax:
			tax.delete_from_db()
			return {'data':{'status': True}}

		return {'data':{'status': False}}

