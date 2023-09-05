#!/usr/bin/python3
'''Contains the blueprint for the API.'''
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
'''The blueprint for the AfyaTech web API.'''


from api.v1.views.hospitals import *
from api.v1.views.doctors import *
from api.v1.views.index import *
from api.v1.views.doctors_hospitals import *
from api.v1.views.patients import *
from api.v1.views.patients_prescriptions import *
from api.v1.views.prescriptions import *
