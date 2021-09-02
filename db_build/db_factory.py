import io
import os
import sqlite3
import numpy as np
import pandas as pd

# this class will create the sqlite3 db

class create_PEAS_db():
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
		CREATE TABLE meta (
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
		CREATE TABLE spectra (
			spec_id INTEGER PRIMARY KEY AUTOINCREMENT,
			id INTEGER,
			wave array,
			spectrum array,
			FOREIGN KEY(id) REFERENCES meta(id)
			);"""

		cur.executescript(command)

		conn.commit()
		conn.close()

	def PEAS_insert(self, meta, wave, spectrum):
		cur, conn = self.open_connection() # create the connection

		command = ("""INSERT INTO meta (UT_date, time_of_obs, object_name, integration_time, grating, central_wavelength, slit_width, phase_angle, comments)
					VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?); """)
		print(meta['UT_date'])
		to_insert = (meta['UT_date'], meta['time_of_obs'], meta['object_name'], meta['integration_time'], meta['grating'], meta['central_wavelength'], meta['slit_width'], meta['phase_angle'], meta['comments'])

		cur.execute(command, to_insert)

		id_ = cur.lastrowid # this will get you the id of the last row that was created from the last meta insert

		command = ("""INSERT INTO spectra (id, wave, spectrum)
					VALUES (?, ?, ?); """)
		to_insert = (id_, wave, spectrum)

		cur.execute(command, to_insert)

		conn.commit()
		conn.close()

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