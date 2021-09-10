# this file is configuration for flask-sqlalchemy if needed in the future

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI = "sqlite:///alchemy_db.sqlite3"
	SQLALCHEMY_TRACK_MODIFICATIONS = False