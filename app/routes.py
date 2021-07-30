from app import app
app.config['SECRET_KEY'] = 'you-will-never-guess'
from flask import render_template, url_for, redirect, request, flash
from flask import jsonify
import numpy as np
from .plots import test_plot

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
		key = key.title()
		if key in all_planets:
			return redirect(url_for('planet', plnt=key))
		else:
			flash('Please enter a planet')
			return redirect(url_for('index'))
	else:
		return render_template('index.html', title='Home')

@app.route('/<plnt>', methods=["POST", "GET"])
def planet(plnt):

	""" This will be the page with all the planet data displayed """

	flux_plot = test_plot(plnt)

	return render_template('planet.html', flux_plot=flux_plot, plnt=plnt, all_planets=all_planets)

@app.route('/planet', methods=['POST', 'GET'])
def change_features_flux_plot():

    """Changes features for the flux/wavelength plot """

    #selected is only defined in the javascript
    selected_planet = request.args['selected_planet']
    print(selected_planet)

    graphJSON= test_plot(selected_planet)

    return graphJSON

@app.route('/contact')
def contact():

	"""This will be contact information"""

	return render_template('contact.html', title='Contact')
