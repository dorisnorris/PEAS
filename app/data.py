import io
import os
import sqlite3
import numpy as np
import pandas as pd

# this class will query the sqlite3 db

class PEAS_db():
	
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
		# this function queries the data needed for the plot on planet.html

		cur, conn = self.open_connection()

		command = (""" SELECT wave, spectrum
					from spectra, meta
					WHERE spectra.id = meta.id and meta.object_name = '{}'; """.format(planet))
	
		cur.execute(command)
		data = cur.fetchall()
		
		conn.close()
		return data

	def get_meta_count(self):
		# this function queries the item count of the meta table

		cur, conn = self.open_connection()

		command = (""" SELECT COUNT(*) FROM meta;""")

		cur.execute(command)
		meta_count = cur.fetchall()

		conn.close()
		return meta_count

	def get_meta_items(self):
		# this function queries all the data in the meta table

		cur, conn = self.open_connection()

		command = (""" SELECT *
					FROM meta;""")

		cur.execute(command)
		meta_items = cur.fetchall()

		conn.close()
		return meta_items

	def get_spectra_count(self):
		# this function queries the item count of the spectra table

		cur, conn = self.open_connection()

		command = (""" SELECT COUNT(*) FROM spectra;""")

		cur.execute(command)
		spectra_count = cur.fetchall()

		conn.close()
		return spectra_count

	def meta_dict(self, meta_items):
		# this function turns the items queried from the meta table and creates a dictionary that will populate the datatable

		table = {'ID':[],
			'UT_Date':[],
			'Time_of_Obs':[],
			'Object_Name':[],
			'Int_Time':[],
			'Grating':[],
			'Central_Wave':[],
			'Slit_Width':[],
			'Phase_Angle':[],
			'Comments':[]}

		for i in meta_items:
			table['ID'] += [i[0]]
			table['UT_Date'] += [i[1]]
			table['Time_of_Obs'] += [i[2]]
			table['Object_Name'] += [i[3]]
			table['Int_Time'] += [i[4]]
			table['Grating'] += [i[5]]
			table['Central_Wave'] += [i[6]]
			table['Slit_Width'] += [i[7]]
			table['Phase_Angle'] += [i[8]]
			table['Comments'] += [i[9]]
		
		return table


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