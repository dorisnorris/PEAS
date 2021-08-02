from app import db

class Main(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	UT_date = db.Column(db.Integer, nullable=False)
	time_of_obs = db.Column(db.Integer)
	object_name = db.Column(db.String(30))
	integration_time = db.Column(db.Integer)
	grating = db.Column(db.Float)
	central_wavelength = db.Column(db.Float)
	slit_width = db.Column(db.Float)
	phase_angle = db.Column(db.Float)
	comments = db.Column(db.String(200))
	spectra = db.relationship('Spectrum', backref='object', lazy=True)

	def __repr__(self):
		return '<Item {}, {}>'.format(self.id, self.object_name) # this needs to be changed at some point

class Spectrum(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	wavelength = db.Column(db.Float)
	flux = db.Column(db.Float)
	main_id = db.Column(db.Integer, db.ForeignKey('main.id'), nullable=False)

	def __repr__(self):
		return '<Spectrum {}, {}>'.format(self.id, self.wavelength, self.flux, self.main_id) # this needs to be changed at some point
