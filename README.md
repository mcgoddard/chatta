chatta
======

A quick and simple chat-room app built in Python using Flask and Sqlalchemy.

## Installation

### Development
To install for development purposes:
1) Install python-virtualenv
2) Initialise a virtual environment in your local repo
	'''
	$ virtualenv venv
	'''
3) Activate the environment using
	'''
	$ . venv/bin/activate
	'''
4) Install dependencies (libmysqlclient-dev, python-dev)
5) Install Python dependencies
	'''
	$ pip install flask-sqlalchemy
	''' 
	This should install flask, sqlalchemy, flask-sqlalchemy, Werkzeug, Jinja2, itsdangerous, markupsafe
4) Install mysql drivers for python (or drivers for whatever database you plan on using)
5) Create empty database for project
6) Set database configuration in "database.py"
7) Run: '''python
	from database import init_db
	init_db()
	'''
8) Start the application running with
	'''
	$ python chatta.py
	'''
9) Access your development site at 127.0.0.1:5000

### Deployment
