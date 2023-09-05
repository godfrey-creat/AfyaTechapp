#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)


@app.route('/doctors', strict_slashes=False)
@app.route('/doctors/<doctor_id>', strict_slashes=False)
def doctors(doctor_id=None):
    """display the doctors listed in alphabetical order"""
    doctors = storage.all("Doctor")
    if doctor_id is not None:
        doctor_id = 'Doctor.' + doctor_id
    return render_template('9-doctors.html', doctors=doctors, doctor_id=doctor_id)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8000')
