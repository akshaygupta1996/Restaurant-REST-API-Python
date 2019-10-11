from flask_restful import Resource, reqparse
from flask import request, jsonify,make_response
from models.users import UsersModel
from models.menuitem import MenuItemModel
from models.userpromo import UserPromoModel
from flask_restful_swagger import swagger
from db import db

import requests
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


class MenuAnalyticsBetweenDates(Resource):



	def get(self, date1, date2):

		result = db.session.execute("SELECT SUM(menu_qty) as qty, menu_item_id from  menuorderitems where menuorderitems.order_no in (select menuorder.id from menuorder where CAST(menuorder.date_time as Date) >= '"+date1 +"' and CAST(menuorder.date_time as date) <= '"+date2 +"') group by menu_item_id ;")

		menu = []

		for re in result:

			r = dict()
			r["menu_qty"] = str(re["qty"])
			r["menu_id"] = str(re["menu_item_id"])
			m = MenuItemModel.find_by_id(re["menu_item_id"])
			if m is not None:

				r["menu_name"] = m.name
				r["menu_description"] = m.description

			menu.append(r)

		return {"data": {"menudata": menu}}