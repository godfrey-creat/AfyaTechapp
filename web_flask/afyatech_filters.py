#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)


@app.route('/afyatech_filters', strict_slashes=False)
def filters():
    """display a HTML page like index.html from static"""
    doctors = storage.all("Doctor").values()
    hospitals = storage.all("Hospital").values()
    return render_template('afyatech_filters.html', doctors=doctors,
                           hospitals=hospitals)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')
