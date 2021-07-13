from flask import render_template, url_for, redirect, request
from app import app

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
		return redirect(url_for('planet', plnt=key))
	else:
		return render_template('index.html', title='Home')

@app.route('/contact')
def contact():

	"""This will be contact information"""

	return render_template('contact.html', title='Contact')

@app.route('/<plnt>', methods=["POST", "GET"])
def planet(plnt):

	""" This will be the page with all the planet data displayed """
	

	return render_template('planet.html', title=plnt, plnt=plnt, all_planets=all_planets)