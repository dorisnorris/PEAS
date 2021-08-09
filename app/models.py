from app import db

class Main(db.Model):
	__tablename__ = "main"
	id = db.Column(db.Integer, primary_key=True)
	UT_date = db.Column(db.Integer, nullable=False)
	time_of_obs = db.Column(db.Integer)
	object_name = db.Column(db.String(30))
	integration_time = db.Column(db.Float)
	grating = db.Column(db.Integer)
	central_wavelength = db.Column(db.Float)
	slit_width = db.Column(db.Integer)
	phase_angle = db.Column(db.Float)
	comments = db.Column(db.String(200))
	spectra = db.relationship('Spectrum', backref='object', lazy=True) # one to many relationship

	def __repr__(self):
		return '<Item {}, {}, {}, {}, {}, {}, {}, {}, {}, {}>'.format(self.id, self.UT_date, self.time_of_obs, self.object_name, self.integration_time, self.grating, self.central_wavelength,
										self.slit_width, self.phase_angle, self.comments) 

class Spectrum(db.Model):
	__tablename__ = "spectrum"
	id = db.Column(db.Integer, primary_key=True)
	wavelength = db.Column(db.Float)
	flux = db.Column(db.Float)
	main_id = db.Column(db.Integer, db.ForeignKey('main.id'), nullable=False)

	def __repr__(self):
		return '<Spectrum {}, {}, {}, {}>'.format(self.id, self.wavelength, self.flux, self.main_id)
