import pandas as pd
import sqlite3

# conn = sqlite3.connect('app.db')

# c = conn.cursor()

mars_spectrum = pd.read_csv('/Users/Doris/Documents/codes/peas/PEAS/app/data/mars_spectrum.dat', delim_whitespace=True, header=None, names=['wavelength','flux'])
print(mars_spectrum)
# mars_spectrum.to_sql(name='Spectrum', con=conn, if_exists='append', index=False )

# conn.commit()
# conn.close()