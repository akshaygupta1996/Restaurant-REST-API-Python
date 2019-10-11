# # import os
# # basedir = os.path.abspath(os.path.dirname(__file__))

# # # SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
# # # SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/kmnorth'
# # #  application.config['SQLALCHEMY_DATABASE_URI'] ='mysql+pymysql://kmnorth7272:kmnorth7272@kmnorth-cluster.cluster-cjyjj0rgxaie.us-west-2.rds.amazonaws.com:3306/kmnorth'
# # # application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# # SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')



# import os
# basedir = os.path.abspath(os.path.dirname(__file__))


# class Config(object):
#     DEBUG = False
#     TESTING = False
#     CSRF_ENABLED = True
#     SECRET_KEY = 'akshay7272'
#     SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/kmnorth'


# class ProductionConfig(Config):
#     DEBUG = False


# class StagingConfig(Config):
#     DEVELOPMENT = True
#     DEBUG = True


# class DevelopmentConfig(Config):
#     DEVELOPMENT = True
#     DEBUG = True


# class TestingConfig(Config):
#     TESTING = True