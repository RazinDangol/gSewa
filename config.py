import os


_cwd = os.path.dirname(os.path.abspath(__file__))
SECRET_KEY = '123sdfas@$%^W$$%ER#@^$T#'
DATABASE = os.path.join(os.getcwd(), 'data.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+DATABASE
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG = True
UPLOAD_FOLDER = os.path.join(os.getcwd(),'upload')
ALLOWED_EXTENSIONS = set(['xls','xlsm','xlsx'])
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'