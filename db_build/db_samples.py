# this file serves as a database study
# we built and compared two databases so far 
# based on efficiency we will move forward with standalone sqlite

import io
import os
import json
import sqlite3
import numpy as np
import pandas as pd
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import Column, Integer, String, Float, ForeignKey, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship,

#all neeed to store the same data
#meta and the spectra

# these functions are so that you can store your float arrays as bytes to minimize storage
def adapt_array(arr):
	out = io.BytesIO()
	np.save(out, arr)
	out.seek(0)

	return sqlite3.Binary(out.read())

def convert_array(text):
	out = io.BytesIO(text)
	out.seek(0)

	return np.load(out)

# the following classes and their functions will build different databases, create tables, inserts, and queries

# this class will create the sqlite3 db
class sqlite3_db():
	#create database using sqlite3
	def __init__(self, filepath):
		self.db_f = os.path.join(filepath)

	def open_connection(self):
		# Create local connection to database as well as return cursor and connection
		try:
			conn = sqlite3.connect(self.db_f, detect_types=sqlite3.PARSE_DECLTYPES)
			# tell sqlite what to do with an array
			sqlite3.register_adapter(np.ndarray, adapt_array) # this will custom code the array datatype
			sqlite3.register_converter("array", convert_array)
			cur = conn.cursor()
			return cur, conn

		except Exception as e:
			print(e)

	def create_db(self):
		""" Creating Database and Database Tables """
		cur, conn = self.open_connection()

		# this creates the meta table
		command = """ DROP TABLE IF EXISTS main;
		CREATE TABLE main (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			UT_date TEXT,
			time_of_obs TEXT,
			object_name TEXT,
			integration_time FLOAT,
			grating INTEGER,
			central_wavelength FLOAT,
			slit_width INTEGER,
			phase_angle FLOAT,
			comments TEXT
			);"""

		cur.executescript(command)

		# this creates the spectra table
		command = """ DROP TABLE IF EXISTS spectrum;
		CREATE TABLE spectrum (
			spec_id INTEGER PRIMARY KEY AUTOINCREMENT,
			id INTEGER,
			wave array,
			spectrum array,
			FOREIGN KEY(id) REFERENCES main(id)
			);"""

		cur.executescript(command)

		conn.commit()
		conn.close()

	def sqlite3_insert(self, meta, wave, spectrum):
		cur, conn = self.open_connection() # create the connection

		command = ("""INSERT INTO main (UT_date, time_of_obs, object_name, integration_time, grating, central_wavelength, slit_width, phase_angle, comments)
					VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?); """)
		print(meta['UT_date'])
		to_insert = (meta['UT_date'], meta['time_of_obs'], meta['object_name'], meta['integration_time'], meta['grating'], meta['central_wavelength'], meta['slit_width'], meta['phase_angle'], meta['comments'])

		cur.execute(command, to_insert)

		id_ = cur.lastrowid # this will get you the id of the last row that was created from the last meta insert

		command = ("""INSERT INTO spectrum (id, wave, spectrum)
					VALUES (?, ?, ?); """)
		to_insert = (id_, wave, spectrum)

		cur.execute(command, to_insert)

		conn.commit()
		conn.close()

	def sqlite3_query(self, planet, time='all', phase_angle='all'):
		cur, conn = self.open_connection()

		command = (""" SELECT * from main, spectrum; """)
		
		cur.execute(command)
		show = cur.fetchall()
		
		conn.close() 
		return show	

# class alchemy_db():
# 	# testing different alchemy method with create engine
# 	def create_db():
# 		engine = create_engine('sqlite:///alchemy_db.sqlite3')

# 		Base = declarative_base()

# 		class Meta(Base):
# 			__tablename__ = "meta"
# 			id = Column(Integer, primary_key=True)
# 			UT_date = Column(Integer, nullable=False)
# 			time_of_obs = Column(Integer)
# 			object_name = Column(String(30))
# 			integration_time = Column(Float)
# 			grating = Column(Integer)
# 			central_wavelength = Column(Float)
# 			slit_width = Column(Integer)
# 			phase_angle = Column(Float)
# 			comments = Column(String(200))
# 			spectrum = relationship('Spectra', backref='object', lazy=True) # one to many relationship

# 		class Spectra(Base):
# 			__tablename__ = "spectra"
# 			id = Column(Integer, primary_key=True)
# 			wavelength = Column(Float)
# 			flux = Column(Float)
# 			meta_id = Column(Integer, ForeignKey('meta.id'), nullable=False)

# 		Base.metadata.create_all(bind=engine)

# 		inspector = inspect(engine)
# 		print(inspector.get_table_names())


# class to create alchemy db and tables
class sqlalchemy_db():
	# create the sqlalchemy database, insert and query functions
	def create_db():
		app = Flask(__name__)
		app.secret_key = "Secret key"
		app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///alchemy_db.sqlite3"
		app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
		db = SQLAlchemy(app)

		class Meta(db.Model): # this will create the meta table
			__tablename__ = "meta"
			id = db.Column(db.Integer, primary_key=True)
			UT_date = db.Column(db.String, nullable=False)
			time_of_obs = db.Column(db.String)
			object_name = db.Column(db.String(30))
			integration_time = db.Column(db.Float)
			grating = db.Column(db.Integer)
			central_wavelength = db.Column(db.Float)
			slit_width = db.Column(db.Integer)
			phase_angle = db.Column(db.Float)
			comments = db.Column(db.String(200))
			spectrum = db.relationship('Spectra', backref='object', lazy=True) # one to many relationship

			#def __repr__(self):
			#	return '<Item {}, {}, {}, {}, {}, {}, {}, {}, {}, {}>'.format(self.id, self.UT_date, self.time_of_obs, self.object_name, self.integration_time, self.grating, self.central_wavelength,
			#								self.slit_width, self.phase_angle, self.comments) 

		class Spectra(db.Model): # this will create the spectra table
			__tablename__ = "spectra"
			id = db.Column(db.Integer, primary_key=True, unique=False)
			wave = db.Column(db.Float)
			flux = db.Column(db.Float)
			meta_id = db.Column(db.Integer, db.ForeignKey('meta.id'), nullable=False)

			# def __repr__(self):
			# 	return '<Spectrum {}, {}, {}, {}>'.format(self.id, self.wavelength, self.flux, self.meta_id)

		db.create_all()
		db.session.commit()

# class to hold alchemy inserts and queries
class grab_sqlalchemy():
	def __init__(self, db_path):
		self.db_path = '/Users/Doris/Documents/codes/peas/PEAS/db_build/alchemy_db.sqlite3'
		self.engine = create_engine(f'sqlite:///{self.db_path}') 

	def alchemy_insert(self, meta, wave, flux):
		db_path = '/Users/Doris/Documents/codes/peas/PEAS/db_build/alchemy_db.sqlite3'
		engine = create_engine(f'sqlite:///{db_path}')
		
		result = engine.execute(f"""INSERT INTO 'meta'(UT_date, time_of_obs, object_name, integration_time, grating, central_wavelength, slit_width, phase_angle, comments)
                     				VALUES ("{meta['UT_date']}", "{meta['time_of_obs']}", "{meta['object_name']}", {meta['integration_time']}, {meta['grating']}, {meta['central_wavelength']}, {meta['slit_width']}, {meta['phase_angle']},"{meta['comments']}");""")

		ID = result.lastrowid

		# for loop to insert wave and spectrum
		for x, y in zip(wave, flux):
			print(x,y)
			result = engine.execute(f"""INSERT INTO 'spectra'(wave, flux, meta_id)
										VALUES ({x}, {y}, {ID});""")

	def alchemy_query(self, planet='all', time='all', phase_angle='all'):
		db_path = '/Users/Doris/Documents/codes/peas/PEAS/db_build/alchemy_db.sqlite3'
		engine = create_engine(f'sqlite:///{db_path}')
		
		result = engine.execute('SELECT * FROM meta;')
		for i in result:
			print(i)

		result2 = engine.execute('SELECT * FROM spectra;')
		for i in result2:
			print(i)

def json_db():
	#create db using json
	return 