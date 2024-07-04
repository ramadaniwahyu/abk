import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config(object):
	"""
	Configuration base, for all environments.
	"""
	DEBUG = True
	TESTING = False
	TEMPLATES_AUTO_RELOAD = True
	PERMANENT_SESSION_LIFETIME = 600
	
	"""
	Database Connection
	"""
	SQLALCHEMY_DATABASE_URI = os.environ.get('URL_DATABASE')
	# SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user123:Q1w2e3r4!!@localhost/db_abk'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	
	BOOTSTRAP_FONTAWESOME = True
	SECRET_KEY = os.environ.get('SECRET_KEY')
	CSRF_ENABLED = True

	UPLOADED_PATH = os.path.join(basedir, 'assets/uploads')

class ProductionConfig(Config):
	DEBUG = False

class DevelopmentConfig(Config):
	DEBUG = True

class TestingConfig(Config):
	TESTING = True
