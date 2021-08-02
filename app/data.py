import sqlite3

conn = sqlite3.connect('peas.db')

c = conn.cursor()

# functions for data handling in Main table

def insert_item(item):
	with conn:
		c.execute("INSERT INTO Main VALUES (:UT_date, :time_of_obs, :object_name, :integration_time, :grating, :central_wavelength, :slit_width, :phase_angle, :comments)",
			{'UT_date': item.UT_date, 'time_of_obs': item.time_of_obs, 'object_name': item.object_name, 'integration_time': item.integration_time, 'grating':item.grating,
			 'central_wavelength': item.central_wavelength, 'slit_width': item.slit_width, 'phase_angle': item.phase_angle, 'comments':item.comments})

def get_item_by_object_name():
	c.execute("SELECT * FROM Main WHERE object_name = :object_name", {'object_name': object_name})
	return c.fetchall()

def remove_item(item):
	with conn:
		c.execute("DELETE from Main WHERE id = :id", {'id': item.id})

# functions for data handling in Spectrum table

def insert_spectrum(item):
	pass

def remove_spectrum(item):
	pass

# close the connection
conn.close()