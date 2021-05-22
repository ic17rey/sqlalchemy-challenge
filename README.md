# SQLAlchemy Challenge - Surfs Up!

## Step 1 - Climate Analysis and Exploration

Python and SQLAlchemy are used to examine a climate database from weather stations in Hawaii. In the jupyter notebook climate.ipynb, tables from an .sqlite file (which is saved to the Resources directory are reflected into classes and saved as 'Station' and 'Measurement'.

### Precipitation Analysis

* Using the most recent date in the dataset, the last 12 months of precipitation data are retrieved and the query select only `date` and `prcp` columns from the class.
* Query results are loaded to a Pandas DataFrame using the date column as the index.
* The DataFrame values are sorted by `date` and then the `plot` method is used to create the plot of precipitation values over time.
* Summary statistics are examined for the data using .describe().

### Station Analysis

* The total number of stations in the dataset are calculated by a query. The stations are listed in descending order by observation count, to identify the most active station.

* For the most active station id, the lowest, highest, and average temperatures are calculated and displayed.  
   * `func.min`, `func.max`, `func.avg` and `func.count` are used in the queries.

* The last 12 months of temperature observation data (TOBS) is retrieved and the data is filtered by the station with the highest number of observations.
  * The results are plotted as a histogram with `bins=12`.

* The session is closed.

## Step 2 - Climate App

A Flask API is created tobased on the queries developed for Step 1. The file is named app.py.

### Routes

* `/` is the Home page and lists all routes that are available.
* `/api/v1.0/precipitation`
  * The query results for precipitation are loaded to a dictionary using `date` as the key and `prcp` as the value, and the dictionary returns for users as a JSON      representation.
* `/api/v1.0/stations`
  * To return a JSON list of stations from the dataset.

* `/api/v1.0/tobs`
  * To query the dates and temperature observations of the most active station for the last year of data, and return as a JSON list of TOBS for the previous year.

* `/api/v1.0/<start>` and `/api/v1.0/<start>/<end>`
  * To return a JSON list of the minimum, average, and the max temperature for a given start or start-end range.
  * When given the start only, needs to calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
  * When given the start and the end date, needs to calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
