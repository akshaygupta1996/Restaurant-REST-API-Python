from flask import Flask
from flask_restful import Api
from flask_restful_swagger import swagger
from resources.users import Users, LoginUsers, UserPhoneNumber, ForgetPassword, ChangePassword
from resources.address import UserAddress, UsersAddress
from resources.menucat import MenuCategory, MenuCategoryEdit
from resources.menumaincat import MenuMainCategory, MenuMainCategoryEdit, MenuItemsByMainCategory
from resources.menuitem import MenuItem, MenuItemEdit
from resources.promocode import PromoCode, PromoCodeEdit, PromoCodeForAll
from resources.userpromo import UserPromo, UserPromoEdit, CheckPromoAvailability, PromoCodeAtCheckOut
from resources.taxes import Tax, TaxEdit
from resources.menuorder import MenuOrderResource, MenuOrderResourceEdit, TestOrderId, MenuOrderResourceEditRatings, MenuOrderForUsers
from resources.admin import LoginAdmin
from resources.cafemenu import CafeMenuResorce, CafePaymentDone
from resources.notification import NotificationConfirmOrder, NotificationKitchen, NotificationOutForDelivery
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from resources.paymentanalytics import DailyPaymentDetails
from resources.sendotp import SendOtpTest
from resources.menuanalytics import MenuAnalyticsBetweenDates
from resources.cafemenu import CafeItemsTest, CafeBookingPaymentConfirmed, CafeOrders
from security import authenticate, identity
from flask_jwt import JWT
import os
import models
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("kmnorth-39c42-firebase-adminsdk-qc7g9-872d9f3775.json")
firebase_admin.initialize_app(cred)




# application = Flask(__name__)

# basedir = os.path.abspath(os.path.dirname(__file__))
# db = models.db


app = Flask(__name__)

db = models.db
# application.config.from_object(os.environ['APP_SETTINGS'])
# application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(application)

# application = Flask(__name__)


# @application.before_first_request
# def create_tables():
# 	db.create_all()


#application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# # 'mysql+pymysql://flaskdemo:flaskdemo@flaskdemo.cwsaehb7ywmi.us-east-1.rds.amazonaws.com:3306/flaskdemo'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/kmnorth2'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://akki7272:akki7272@fooddelivery.ceckddzhbyhp.us-west-2.rds.amazonaws.com:3306/kmnorth2'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://akshay7272:akshay7272@kmnorth2.ceckddzhbyhp.us-west-2.rds.amazonaws.com:3306/km'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kmnorth007:kmnorth007@kmnorth.crx51qhsnwjl.us-east-2.rds.amazonaws.com:3306/kmnorth2'

 # application.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://kmnorth7272:kmnorth7272@kmnorth-cluster.cluster-cjyjj0rgxaie.us-west-2.rds.amazonaws.com:3306/kmnorth'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'akshay7272'
api = Api(app)
api = swagger.docs(Api(app), apiVersion='0.1')
jwt = JWTManager(app)


migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
# jwt = JWT(application, authenticate, identity) # /auth
# db = SQLAlchemy(application)
# db.init_app(app)





api.add_resource(Users, '/register')
api.add_resource(LoginUsers, '/login/<int:flag>/<string:user_ep>/<string:password>/<string:fcmtoken>')
api.add_resource(UsersAddress, '/user_address/<int:user_id>')
api.add_resource(UserAddress, '/address/<int:id>')
api.add_resource(MenuCategory, '/category/<int:main_cat_id>')
api.add_resource(MenuCategoryEdit, '/category/<int:cat_id>')
api.add_resource(MenuItem,'/menuitem')
api.add_resource(MenuItemEdit, '/menuitem/<int:id>')
api.add_resource(PromoCode,'/promocode')
api.add_resource(PromoCodeEdit,'/promocode/<int:promo_id>')
api.add_resource(UserPromoEdit,'/userpromo/<int:userpromo_id>')
api.add_resource(UserPromo,'/userpromoedit/<int:user_id>')
api.add_resource(MenuMainCategory, '/menumaincat')
api.add_resource(MenuMainCategoryEdit, '/menumaincat/<int:cat_id>')
api.add_resource(MenuItemsByMainCategory, '/menu')
api.add_resource(Tax, '/tax')
api.add_resource(TaxEdit, '/tax/<int:id>')
api.add_resource(PromoCodeForAll, '/promocodeforall')
api.add_resource(CheckPromoAvailability, '/checkpromoavailability/<string:promo_code>/<int:user_id>')
api.add_resource(PromoCodeAtCheckOut, '/phomocodeatcheckout/<int:user_id>')
api.add_resource(MenuOrderResource, '/bookmenu')
api.add_resource(MenuOrderResourceEdit, '/approveorder/<int:order_id>')
api.add_resource(MenuOrderResourceEditRatings, '/foodratings/<int:order_id>/<int:ratings>')
api.add_resource(MenuOrderForUsers, '/menuorderusers/<int:user_id>')
api.add_resource(LoginAdmin, '/admin/<string:username>/<string:password>/<string:fcmtoken>')
api.add_resource(NotificationConfirmOrder, '/confirmorder/<int:user_id>/<int:order_id>')
api.add_resource(NotificationKitchen, '/inkitchen/<int:user_id>/<int:order_id>')
api.add_resource(NotificationOutForDelivery, '/outfordelivery/<int:user_id>/<int:order_id>')
api.add_resource(DailyPaymentDetails, '/paymentanalytics/<string:dateone>/<string:datetwo>')
api.add_resource(TestOrderId, '/testorder')
api.add_resource(CafeMenuResorce, '/cafemenu')
api.add_resource(CafePaymentDone, '/cafepaymentsuccess/<string:order_id>')
api.add_resource(UserPhoneNumber,'/changephonenumber/<int:user_id>/<string:alt_phone_number>')
api.add_resource(CafeItemsTest, '/cafeitemtest')
api.add_resource(CafeBookingPaymentConfirmed, '/cafepaymentconfirm/<int:order_id>')
api.add_resource(CafeOrders, '/cafeorders/<string:date>')
api.add_resource(SendOtpTest,'/sendotp/<string:phone_number>')
api.add_resource(MenuAnalyticsBetweenDates, '/menubetweendates/<string:date1>/<string:date2>')
api.add_resource(ForgetPassword, '/forgetpassword/<string:phone_number>')
api.add_resource(ChangePassword, '/changepassword/<int:user_id>/<string:password>/<string:new_password>')

if __name__ == '__main__':
	# from db import db
	db.init_app(app) 
	
	 #we are importing here due to circular imports
	manager.run()