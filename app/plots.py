import plotly
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import json

def test_plot():
	x = np.arange(10)
	fig = go.Figure(data=go.Scatter(x=x, y=x**2))

	fig.update_layout(
                 xaxis_title="X axis",
                 yaxis_title="Y axis",
                 title= "Title")

	return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
