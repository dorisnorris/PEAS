import os
import plotly
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import json

def test_plot(selected_planet, peas_db):
	# directory = '/Users/Doris/Documents/codes/peas/PEAS/app/data/Albedos'

	if isinstance(selected_planet, str):
		selected_planet = [selected_planet]

	if len(selected_planet) == 0:
		title= "None Selected"
		print(title)
	elif len(selected_planet) == 1:
		title= selected_planet[0]
		print(title)
	elif len(selected_planet) == 2:
		title= ' and '.join(selected_planet)
		print(title)
	elif len(selected_planet) > 2:
		title=  selected_planet[0] + ', ' + selected_planet[1] + ', and ' + selected_planet[2]
		print(title)

	fig = go.Figure()

	for i in selected_planet:
		# read_in = pd.read_csv(os.path.join(directory, f'{i}.txt'), header=None, names=['w', 'f'], delim_whitespace=True)
		data = peas_db.get_data(i)
		# print(data)

		for row in data:
			x, y = row
			# print('wavelength:', x, 'flux:', y)

			fig.add_trace(go.Scatter(
						x = x/np.max(x),
						y = y/np.max(y),
						mode = 'lines',
						name = i))

			fig.update_layout(
	            	xaxis_title="Wavelength",
	          		yaxis_title="Flux",
	           		title= title)

	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON

