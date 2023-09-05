#!/usr/bin/python3
"""
starts a Flask web application
"""

from flask import Flask, render_template
from models import *
from models import storage
app = Flask(__name__)


@app.route('/hospitals_list', strict_slashes=False)
def hospitals_list():
    """display a HTML page with the hospitals listed in alphabetical order"""
    hospitals = sorted(list(storage.all("Hospital").values()), key=lambda x: x.name)
    return render_template('hospitals_list.html', hospitals=hospitals)


@app.teardown_appcontext
def teardown_db(exception):
    """closes the storage on teardown"""
    storage.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')
