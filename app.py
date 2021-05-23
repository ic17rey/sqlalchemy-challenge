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

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the precipitation measurements table
Measurement = Base.classes.measurement

# Save reference to the stations table
Station = Base.classes.station

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
        f'/api/v1.0/start<start>/<br/>'
        f'/api/v1.0/start/end<start>/<end>'
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
    print('Server received request for precipitation page')
    # Create our session (link) from Python to database
    session = Session(engine)
    
    # Copy in the year_prior variable already created in the jupyter notebook
    year_prior = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    # Perform a query to retrieve the date and precipitation values
    results = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= year_prior).\
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

@app.route('/api/v1.0/stations')
def weather_stations():
    print('Server received request for stations page')

    # Create our session (link) from Python to database
    session = Session(engine)
    
    # Query for and group by measurement stations to display each station only once
    results_stations = session.query(Measurement.station).group_by(Measurement.station).all()
    
    session.close()
    
    all_stations = list(np.ravel(results_stations))

    return jsonify(all_stations)
 
@app.route('/api/v1.0/tobs')
def tobs_query():
    print('Server received request for tobs page')
    
    # Create our session (link) from Python to database
    session = Session(engine)
    
    # Copy in the year_prior variable already created in the jupyter notebook
    year_prior = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    
    selections = [Measurement.station,
        func.count(Measurement.tobs),
        func.min(Measurement.tobs),
        func.max(Measurement.tobs),
        func.avg(Measurement.tobs)] 
    most_active_analysis = session.query(*selections).filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= year_prior).all()
    session.close()

    return jsonify(most_active_analysis)

if __name__ == '__main__':
    app.run(debug=True)
