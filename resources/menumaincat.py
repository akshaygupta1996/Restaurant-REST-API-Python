from flask_restful import Resource, reqparse
from flask import request
from models.menumaincat import MenuMainCategoryModel
from models.menucat import MenuCategoryModel
from models.menuitem import MenuItemModel
from flask_restful_swagger import swagger
import json
from flask import jsonify


class MenuMainCategory(Resource):

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
			}]
		)
	def post(self):

		data = MenuMainCategory.parser.parse_args()
		menu_cat = MenuMainCategoryModel(data['cat_name'])
		try:
			menu_cat.save_to_db()
		except:
			return {'data':{"status": False, 'message': 'Error Occured'}}, 500
		
		return {'data':{'status': True, 'maincategory': menu_cat.json()}}, 201

	@swagger.operation(
		notes='Get List of all Main Menu Category',
		nickname='GET'
		)
	def get(self):

		return {'data':{'status':True, 'category': [category.json() for category in MenuMainCategoryModel.query.all()]}}


class MenuMainCategoryEdit(Resource):

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

		data = MenuMainCategoryEdit.parser.parse_args()
		menu_cat = MenuMainCategoryModel.find_by_id(cat_id)
		if menu_cat:
			menu_cat.cat_name = data['cat_name']
			menu_cat.save_to_db()
			return {'data':{'status': True, 'data': menu_cat.json()}}

		return {'data':{'status': False, 'error': "Invalid Id"}}

	@swagger.operation(
		notes='List all sub menu Category in the category',
		nickname='GET',
		parameters=[
			{
				"name": "cat_id",
				"required": True,
				"dataType": "int"
			}]
		)

	def get(self, cat_id):
		return {'data': {'status':True, 'category':[cat.json() for cat in MenuCategoryModel.query.filter_by(main_cat_id = cat_id).all()]}}



class MenuItemsByMainCategory(Resource):


	@swagger.operation(
		notes='List all items with category in main category',
		nickname='GET',
		parameters=[
			{
				"name": "cat_id",
				"required": True,
				"dataType": "int"
			}]
		)


	def get(self):

		maincategory , category, items, cc = [], [] ,[], []

		maincat = MenuMainCategoryModel.query.all()

		for main in maincat:
			print main.json()
			category, items = [], []
			maincategory.append(main.json())
			allcat = MenuCategoryModel.query.filter_by(main_cat_id = main.id).all()
			for cat in allcat:
				category.append(cat.json())
				menuitems = MenuItemModel.query.filter_by(cat_id = cat.id).all()
				m_items = []
				for item in menuitems:
					m_items.append(item.json())
				items.append(m_items)
			all_menu_items = [{"subcategory": t, "items": s} for t,s in zip(category, items)]
			cc.append(all_menu_items)

		fuck_all_menu = [{"maincategory": m, "allitems": c} for m,c in zip(maincategory, cc)]
		return {'data':{'status': True, 'menu': fuck_all_menu}}



		# allcat = MenuCategoryModel.query.filter_by(main_cat_id = cat_id).all()

		# for cat in allcat:
		# 	print cat.json()
		# 	category.append(cat.json())
		# 	menuitems = MenuItemModel.query.filter_by(cat_id = cat.id).all()
		# 	m_items = []
		# 	for item in menuitems:
		# 		m_items.append(item.json())
		# 	items.append(m_items)

		# all_menu_items = [{"category": t, "items": s} for t, s in zip(category, items)]
		# # print items
		# # all_menu_items = {"items": [s for s in items]}

		# return {'data':{'status': True, 'menu': all_menu_items}}