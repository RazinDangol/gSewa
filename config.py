import os


_cwd = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(os.getcwd(), 'data.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+DATABASE
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG = True
UPLOAD_FOLDER = os.path.join(os.getcwd(),'upload')
ALLOWED_EXTENSIONS = set(['xls','xlsm','xlsx'])