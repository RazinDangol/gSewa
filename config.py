import os

_cwd = os.path.dirname(os.path.abspath(__file__))
print(_cwd)
SECRET_KEY = '123sdfas@$%^W$$%ER#@^$T#'
DATABASE = os.path.join(_cwd, 'data.db')
UPLOAD_FOLDER = os.path.join(_cwd,'upload')
SQLALCHEMY_DATABASE_URI = 'sqlite:///'+DATABASE
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
DEBUG = True

ALLOWED_EXTENSIONS = set(['xls','xlsm','xlsx'])
CELERY_BROKER_URL = os.getenv('REDIS_URL','redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL','redis://localhost:6379/0')
CELERY_TASK_SERIALIZER = 'json'
