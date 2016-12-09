from flask import render_template, flash, redirect, session, url_for, request,g
from app import app, db
from .forms import LoginForm
from .models import User, Post, Timeseries
import json

import socket
import sys
import pickle


@app.route('/')
@app.route('/index')
def index():
	
	user = {'nickname': 'Kevin'}
	posts = [
	{
		'author': {'nickname':'John'},
		'body': 'Beautiful day in Portland!'
	},
	{
		'author': {'nickname': 'Susan'},
		'body': 'The movie was cool!'
	}
	]
	return render_template('index.html',
							title='Home',
							user=user,
							posts=posts)

@app.route('/success/<name>')
@app.route('/success')
def success(name=None):
	return 'welcome %s' % name

@app.route('/login', methods=['POST','GET'])
def login():
	print("HIIII")
	if request.method == 'POST':
		user = request.form['nm']
		return redirect(url_for('success', name=user))
	else:
		user = request.args.get('nm')
		# blah = request.args.get('blah')
		# print(user,blah)
		return redirect(url_for('success', name=user))

@app.route('/loginPage')
def loginPage():
	return render_template('login.html',
		title='Login'
		)

@app.route('/createUser', methods=['GET'])
def createUser():
	u = User(nickname='keasadvin',email='ka@gmail.com')
	db.session.add(u)
	db.session.commit()
	print("Added user to db!")
	return json.dumps({"1":"1"});
	

@app.route('/timeseries', methods=['POST','GET'])
def timeseries():
	if request.method == 'POST':
		# adds a new timeseries into the database given a json which has a
		#  key for an id and a key for the timeseries, and returns the timeseries
		port = 12340 
		s = socket.socket()
		host = socket.gethostname()

		s.connect((host, port))
		print("Connected to ",host," ",port)
		try:
			while True:
				toSend = input("Enter something to send to server: ")
				test = {"time":[1,2,3],"value":[3,4,5]}
				s.send(pickle.dumps(test))
		finally:
			s.close()
		
	else:
		# should send back a json with metadata from all the time series

		# Get query parameters
		# mean_in = request.args.get('mean_in')
		# if mean_in is not None:
		# 	mean_in = mean_in.split('-')
		# 	m_min, m_max = float(mean_in[0]),float(mean_in[1])
		# level_in = request.args.get('level_in')

		# if level_in is not None:
		# 	level_in = level_in.split(',') 

		# level = request.args.get('level')
		# return json.dumps({"1":"1"});
		results = Timeseries.query.all()
		# jsonFile = {}
		# print("Timeseries",results[0].serialize())
		r = [e.serialize() for e in results]
		print("R=",r)
		return json.dumps(r)
	
@app.route('/simquery', methods=['POST','GET'])
def simquery():
	if request.method == 'POST':
		# take a timeseries as an input in a JSON, carry out the query, and 
		# return the appropriate ids as well. 
		ts = request.form['timeseries'] # json format
		pass
	else:
		#  take a id=the_id querystring and use that as an id into the database
		# to find the timeseries that are similar, sending back the ids of (say) the top 5
		sim_id = request.args.get('id')
		pass
		

@app.route('/timeseries/<id>')
def timeseries_id(id):
	# should send back metadata and the timeseries itself in a JSON payload
	return json.dumps({"metadata":id, 
						"timeseries":{
							"time":{"0":"1"},
							"values":{"0":"11"}
						}});
