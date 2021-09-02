import io
import os
import sqlite3
import numpy as np
import pandas as pd

# this class will create the sqlite3 db

class PEAS_db():
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

	def get_data(self, planet, time='all', phase_angle='all'):
		'''
		Currently, this will query all data from meta table and spectra table
		'''
		cur, conn = self.open_connection()

		command = (""" SELECT * from meta, spectra; """)
	
		cur.execute(command)
		data = cur.fetchall()
		
		conn.close() 
		return data	

# these functions below are so that you can store your float arrays as bytes to minimize storage

def adapt_array(arr):
	out = io.BytesIO()
	np.save(out, arr)
	out.seek(0)

	return sqlite3.Binary(out.read())

def convert_array(text):
	out = io.BytesIO(text)
	out.seek(0)

	return np.load(out)