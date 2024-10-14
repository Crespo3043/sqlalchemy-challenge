# Import the dependencies.
import numpy as np
import datetime as dt

# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# Import Flask
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect the existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    """List all available API routes."""
    return (
        f"Welcome to SurfsUp API<br/>"
        f"Available Routes:<br/>"
        f"_______________________<br/>"
        f"Precipitation data for last 12 months (2016-08-24 to 2017-08-23):<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"_______________________<br/>"
        f"List of stations in the dataset:<br/>"
        f"/api/v1.0/stations<br/>"
        f"_______________________<br/>"
        f"Date and temperature observations of the most-active station (USC00519281) for previous year:<br/>"
        f"/api/v1.0/tobs<br/>"
        f"_______________________<br/>"
        f"Minimum, Maximum and average temperature from a given start date to end of dataset:<br/>"
        f"Please enter Start Date in the format: YYYY-MM-DD<br/>"
        f"/api/v1.0/<start><br/>"
        f"_______________________<br/>"
        f"Minimum, Maximum and average temperature from a given start date to a given end date:<br/>"
        f"Please enter Start Date and End Date in the format: YYYY-MM-DD/YYYY-MM-DD<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"_______________________"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    """Retrieve last 12 months of data"""

    # Convert the query results from your precipitation analysis 
    # (i.e. retrieve only the last 12 months of data) to a dictionary 
    # using date as the key and prcp as the value.

    # Find the most recent date in the dataset.
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date

    # Calculate the date one year from the last date in data set.
    year_ago_date = dt.datetime.strptime(latest_date, '%Y-%m-%d') - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    prcp_scores = session.query(Measurement.date, Measurement.prcp).\
                    filter(Measurement.date >= year_ago_date).\
                    order_by(Measurement.date).all()
    
    # Close the session
    session.close()
    
    # Create a dictionary using date as the key and prcp as the value
    prcp_dict = {}
    for date, prcp in prcp_scores:
        prcp_dict[date] = prcp
    
    # Return the JSON representation of dictionary.
    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    """Get a list of stations"""

    # Perform a query to retrieve the station data
    station_data = session.query(Station.station).all()
    
    # Close the session
    session.close()
    
    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_data))
    
    # Return a JSON list of stations from the dataset.
    return jsonify(station_list)
