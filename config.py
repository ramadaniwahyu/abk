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
	SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@localhost/db_abk'
	#SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user_db:Q1w2e3r4!!@192.168.20.1/pkpo'
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	
	BOOTSTRAP_FONTAWESOME = True
	SECRET_KEY = "AFSBAKFBAKBFAK09876543TNJQN!$@y(!$yGABV"
	CSRF_ENABLED = True

class ProductionConfig(Config):
	DEBUG = False

class DevelopmentConfig(Config):
	DEBUG = True

class TestingConfig(Config):
	TESTING = True
