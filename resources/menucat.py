from flask_restful import Resource, reqparse
from flask import request
from models.menucat import MenuCategoryModel
from models.menuitem import MenuItemModel
from flask_restful_swagger import swagger


class MenuCategory(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('cat_name',
			type = str,
			required = True,
			help = "Category Name is Required"
		)
	@swagger.operation(
		notes='Adding A Menu Category',
		nickname='POST',
		parameters=[
			{
				"name": "cat_name",
				"required": True,
				"dataType": "string"
			},
			{
				"name": "main_cat_id",
				"required": True,
				"dataType": "int"
			}]
		)
	def post(self, main_cat_id):

		data = MenuCategory.parser.parse_args()
		menu_cat = MenuCategoryModel(main_cat_id,data['cat_name'])
		try:
			menu_cat.save_to_db()
		except:
			return {'data':{"status": False, 'message': 'Error Occured'}}, 500
		
		return {'data':{'status': True, 'subcategory': menu_cat.json()}}, 201

	# @swagger.operation(
	# 	notes='Get List of all Menu Category',
	# 	nickname='GET'
	# 	)
	# def get(self):

	# 	return {'category': [category.json() for category in MenuCategoryModel.query.all()]}


class MenuCategoryEdit(Resource):

	parser = reqparse.RequestParser()
	parser.add_argument('cat_name',
			type = str,
			required = True,
			help = "Category Name is Required"
		)

	@swagger.operation(
		notes='Edit A Menu Category',
		nickname='PUT',
		parameters=[
			{
				"name": "cat_name",
				"required": True,
				"dataType": "string"
			}]
		)

	def put(self, cat_id):

		data = MenuCategoryEdit.parser.parse_args()
		menu_cat = MenuCategoryModel.find_by_id(cat_id)
		if menu_cat:
			menu_cat.cat_name = data['cat_name']
			menu_cat.save_to_db()
			return {'data':{'status': True, 'subcategory': menu_cat.json()}}

		return {'data':{'status': False, 'error': "Invalid Id"}}

	@swagger.operation(
		notes='List all menu items in the category',
		nickname='GET',
		parameters=[
			{
				"name": "cat_id",
				"required": True,
				"dataType": "int"
			}]
		)

	def get(self, cat_id):
		return {'data': {'status':True, 'items': [item.json() for item in MenuItemModel.query.filter_by(cat_id = cat_id).all()]}}


	@swagger.operation(
		notes='Delete a Menu Sub Category',
		nickname='DELETE',
		parameters=[
			{
				"name": "cat_id",
				"required": True,
				"dataType": "int"
			}]
		)

	def delete(self, cat_id):

		item = MenuCategoryModel.find_by_id(cat_id)
		if item:
			item.delete_from_db()
			return {'data':{'status': True}}
		return {'data':{'status': False}}

