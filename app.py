#################
# Part II: Flask
#################

# Setup dependencies for working with hawaii.sqli
import os
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

# Import Flask
from logging import debug
from flask import Flask, jsonify

# Database Setup
database_path = os.path.join('Resources', 'hawaii.sqlite')
engine = create_engine(f'sqlite:///{database_path}')

# db_file = os.path.dirname(__file__)
# engine = create_engine(f'sqlite:///{db_file}/Resources/hawaii.sqlite')
# for using both?
# engine = create_engine(f'sqlite:///{db_file}/{database_path}')


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the precipitation measurements table
Measurement = Base.classes.measurement

# Create an app, passing the __name__
app = Flask(__name__)

# Define reaction for when a user hits the index route
@app.route('/')
def home():
    print('Server received request for "Home" page...')
    return (
        f'Welcome to the Home page for the SQLAlchemy Challenge!<br/>'
        f'<br/>'
        f'At various stations in Hawaii precipitation and temperatures are measured.<br/>'
        f'More information and these measurements can be discovered by using the following available routes:<br/>'
        f'/about<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start>/<br/>'
        f'/api/v1.0/<start>/<end>'
    )

@app.route('/about')
def about():
    student_name = 'Lindsay Reynolds'
    course = 'Butler Data Analytics, Spring/Summer 2021'
    challenge_name = 'SQL Alchemy Challenge'
    print('Server received request for "About" page')
    return (
        f'Welcome to the "About" page for the {challenge_name}!<br/>'
        f'<br/>'
        f'The challenge is being completed by {student_name} for {course}.'   
    )

@app.route('/api/v1.0/precipitation')
def precip():
    # Create our session (link) from Python to database
    session = Session(engine)
    
    # Copy in the year_prior variable already created in the jupyter notebook
    year_prior = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the date and precipitation values
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date > year_prior).\
        order_by(Measurement.date.desc()).all()

    session.close()

    # Convert the query results to a dictionary
    # Use date as the key and prcp as the value
    all_precip = []
    for date, prcp in results:
        precip_dict = {}
        precip_dict = {date: prcp}
        all_precip.append(precip_dict)

    # Return the dictionary representation in JSON
    return jsonify(all_precip)

# @app.route('/api/v1.0/stations')
# def station_ids():

# @app.route('/api/v1.0/tobs')
       

if __name__ == '__main__':
    app.run(debug=True)
