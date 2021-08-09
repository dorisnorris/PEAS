from app import app, db
from app.models import Main, Spectrum

@app.shell_context_processor
def make_shell_context():
	return {'db': db, 'Main': Main, 'Spectrum': Spectrum}