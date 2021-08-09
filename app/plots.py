import plotly
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import json

def test_plot(selected_planet):

	x = np.arange(10)
	fig = go.Figure(data=go.Scatter(x=x, y=x**2))

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

	fig.update_layout(
                 xaxis_title="Wavelength",
                 yaxis_title="Flux",
                 title= title)

	graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

	return graphJSON

