#################
# Part II: Flask
#################

# Import Flask
from logging import debug
from flask import Flask

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
        f'<br/>'
        f'These measurements can be examined by using the following available routes:<br/>'
        f'/about<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/stations<br/>'
        f'/api/v1.0/tobs<br/>'
        f'/api/v1.0/<start><br/>'
        f'/api/v1.0/<start>/<end>'
    )

@app.route('/about')
def about():
    print('Info about the page')
    return 'Welcome to the "About" page for the SQLAlchemy Challenge!'   

if __name__ == '__main__':
    app.run(debug=True)
