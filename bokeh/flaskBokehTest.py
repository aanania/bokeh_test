from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
import MySQLdb

app = Flask(__name__)

# Load the Iris Data Set
feature_names = ["Histogram"]
local_ip = "139.229.136.31"

# Create the main plot
def create_figure():

	data = queryData("select Calibrated_1, date_time from rotator_Position;")
	dataCMD = queryData("select angle, date_time from rotator_command_track;")
	data_type = [('position', np.float),
		     ('date', '<M8[us]')]
	data2 = np.fromiter(data, count=-1, dtype=data_type)
	data2CMD = np.fromiter(dataCMD, count=-1, dtype=data_type)
	p1 = figure(title="Rotator position")

	x1 = data2['date']
	y1 = data2['position']

	x2 = data2CMD['date']
	y2 = data2CMD['position']

	p1.line(x1, y1, line_color="blue", line_width=2, alpha=1, legend="Position")
	p1.line(x2, y2, line_color="red", line_width=2, alpha=1, legend="Position CMD")

	p1.legend.location = "center_right"
	p1.legend.background_fill_color = "darkgrey"
	p1.xaxis.axis_label = 'Date'
	p1.yaxis.axis_label = 'Position in degrees'

	return p1

def queryData(query):
	db = MySQLdb.connect(host=local_ip,    # your host, usually localhost
		             user="efduser",         # your username
		             passwd="lssttest",  # your password
		             db="EFD")        # name of the data base

	cur = db.cursor()
	cur.execute(query)
	data = cur.fetchall()
	db.close()
	return data

# Index page
@app.route('/')
def index():
	# Determine the selected feature
	current_feature_name = request.args.get("feature_name")
	if current_feature_name == None:
		current_feature_name = "Sepal Length"

	# Create the plot
	plot = create_figure()
		
	# Embed plot into HTML via Flask Render
	script, div = components(plot)
	return render_template("rotator.html", script=script, div=div,
		feature_names=feature_names,  current_feature_name=current_feature_name)

# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
	app.run(host= '0.0.0.0', port=80, debug=True)
