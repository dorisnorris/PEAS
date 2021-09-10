from app import app
import numpy as np
app.config['SECRET_KEY'] = 'you-will-never-guess'
from flask import render_template, url_for, redirect, request, flash
from flask import jsonify
from .plots import test_plot
from .data import PEAS_db as PEASdb

peas_db = PEASdb('/Users/Doris/Documents/codes/peas/PEAS/app/data/PEAS.db') # this probably needs to be edited

# this is a dict that is used to verify the users input in the index is a planet
# it is also used to populate the dropdown menu in the planet page
all_planets = {
				'Mercury' : 1,
				'Venus' : 2,
				'Earth' : 3,
				'Mars' : 4,
				'Jupiter': 5,
				'Saturn' : 6,
				'Uranus' : 7,
				'Neptune' : 8}

@app.route('/')
@app.route('/index', methods=["POST", "GET"])
def index():

	""" Main landing page """

	if request.method == "POST":
		key = request.form['keyword']
		key = key.title() # this takes the users input and capitalizes the first letter
		if key in all_planets:
			print(key) # debugging
			return redirect(url_for('planet', plnt=key))
		else:
			flash('Please enter a planet') # this is an error message that displays if user inputs nothing or not a planet
			return redirect(url_for('index'))
	else:
		return render_template('index.html', title='Home')

@app.route('/<plnt>', methods=["POST", "GET"])
def planet(plnt):

	""" This will be the page with all the planet data displayed """

	flux_plot = test_plot(plnt, peas_db)

	return render_template('planet.html', flux_plot=flux_plot, plnt=plnt, all_planets=all_planets)

@app.route('/planet', methods=['POST', 'GET'])
def change_features_flux_plot():

    """Changes features for the flux/wavelength plot """

    selected_planet = request.args['selected_planet'] #selected is only defined in the javascript
    selected_planet = eval(selected_planet)
    print(selected_planet)

    graphJSON= test_plot(selected_planet, peas_db)

    return graphJSON

@app.route('/data')
def data():

	"""This will be data information that is queried from the db"""

	meta_count = peas_db.get_meta_count() # testing queries
	meta_items = peas_db.get_meta_items()
	table = peas_db.meta_dict(meta_items) # this gets a table dict from data.py to populate the datatable
	print(table) # debugging

	spectra_count = peas_db.get_spectra_count() # testing queries

	print("Total number of meta items is : {}".format(meta_count)) # debugging into terminal
	# print(type(meta_count))
	# print(type(meta_items))

	return render_template('data.html', title='data', all_planets=all_planets, meta_count=meta_count, meta_items=meta_items, spectra_count=spectra_count, data=data, meta=table, table_len=len(table))
