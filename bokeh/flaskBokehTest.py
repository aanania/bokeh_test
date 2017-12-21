from flask import Flask, render_template, request
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from datetime import datetime as dt
from bokeh.models import DatetimeTickFormatter

from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, DateField

import MySQLdb

app = Flask(__name__)

# Load the Iris Data Set
feature_names = ["Angle_check", "Velocity_check"]
local_ip = "139.229.136.31"
angle_limit = 60

# Create the main plot
def create_figure(initial_date, end_date):

	queryRotator = "SELECT Calibrated_1, date_time FROM rotator_Position WHERE date_time BETWEEN \"%s\" AND \"%s\";" % (initial_date, end_date)
	queryRotCommand = "SELECT angle, date_time FROM rotator_command_track WHERE date_time BETWEEN \"%s\" AND \"%s\";" % (initial_date, end_date)

	#print(queryRotator)
	#print(queryRotCommand)

	data = queryData(queryRotator)
	dataCMD = queryData(queryRotCommand)
	data_type = [('position', np.float),
		     ('date', '<M8[us]')]
	data2 = np.fromiter(data, count=-1, dtype=data_type)
	data2CMD = np.fromiter(dataCMD, count=-1, dtype=data_type)
	p1 = figure(title="Rotator position", x_axis_type='datetime')

	x1 = data2['date']
	y1 = data2['position']
	#print(x1)
	x2 = data2CMD['date']
	y2 = data2CMD['position']

	#index_greater_pos =  np.where(y1 > angle_limit)
	#index_greater_cmd =  np.where(y2 > angle_limit)
	#index_smaller_pos =  np.where(y1 < angle_limit)
	#index_smaller_cmd =  np.where(y2 < angle_limit)

	#x3 = [x1[index_greater_pos], x1[index_smaller_pos]]
	#y3 = [y1[index_greater_pos], y1[index_smaller_pos]]

	#x4 = [x2[index_greater_cmd], x2[index_smaller_cmd]]
	#y4 = [y2[index_greater_cmd], y2[index_smaller_cmd]]

	#p1.multi_line( x3, y3, color=["red","blue"], line_width=2, alpha=[0.5, 0.5] , legend="Position")
	p1.line( x1, y1, color="blue", line_width=2, alpha=0.5 , legend="Position")
	p1.line( x2, y2, color="green", line_width=2, alpha=0.5, legend="Position CMD")

	p1.line( [x1[0], x1[-1]], [angle_limit, angle_limit], line_color="red", line_width=1, alpha=0.5)

	#p1.line( x1[index_greater_pos], y1[index_greater_pos], line_color="red", line_width=2, alpha=1, legend="Position out of limit")
	#p1.line( x2[index_greater_cmd], y2[index_greater_cmd], line_color="brown", line_width=2, alpha=1, legend="Cmd out of limit")

	
	
	#p1.xaxis.formatter=DatetimeTickFormatter(hours=["%d %B %Y"],days=["%d %B %Y"],months=["%d %B %Y"],years=["%d %B %Y"],)

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
@app.route('/', methods=['POST','GET'])
def index():
	# Determine the selected feature
	current_feature_name = request.args.get("feature_name")
	if(request.method == 'POST'):
		initial_date = request.form["initial_date"]
		end_date = request.form["end_date"]
		# Create the plot
		
		print(initial_date)
		print(end_date)
	else:
		initial_date = 0 
		end_date = 0 

	plot = create_figure(initial_date, end_date)
	if current_feature_name == None:
		current_feature_name = "Angle_check"


		
	# Embed plot into HTML via Flask Render
	script, div = components(plot)
	return render_template("rotator.html", script=script, div=div,
		feature_names=feature_names,  current_feature_name=current_feature_name)

# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
	app.run(host= '0.0.0.0', port=80, debug=True)
