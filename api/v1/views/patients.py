#!/usr/bin/python3
'''Contains the users view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, BadRequest

from api.v1.views import app_views
from models import storage
from models.patient import Patient


@app_views.route('/patients', methods=['GET'])
@app_views.route('/patients/<patient_id>', methods=['GET'])
def get_patients(patient_id=None):
    '''Gets the patient with the given id or all users.
    '''
    if patient_id:
        patient = storage.get(Patient, patient_id)
        if patient:
            obj = patient.to_dict()
            if 'hospitals' in obj:
                del obj['hospitals']
            if 'prescriptions' in obj:
                del obj['prescriptions']
            return jsonify(obj)
        raise NotFound()
    all_patients = storage.all(Patient).values()
    patients = []
    for patient in all_patients:
        obj = patient.to_dict()
        if 'hospitals' in obj:
            del obj['hospitals']
        if 'prescriptions' in obj:
            del obj['prescriptions']
        patients.append(obj)
    return jsonify(patients)


@app_views.route('/patients/<patient_id>', methods=['DELETE'])
def remove_patient(patient_id):
    '''Removes a patient with the given id.
    '''
    patient = storage.get(Patient, patient_id)
    if patient:
        storage.delete(patient)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


@app_views.route('/patients', methods=['POST'])
def add_patient():
    '''Adds a new patient.
    '''
    data = {}
    try:
        data = request.get_json()
    except Exception:
        data = None
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'email' not in data:
        raise BadRequest(description='Missing email')
    if 'password' not in data:
        raise BadRequest(description='Missing password')
    patient = Patient(**data)
    patient.save()
    obj = patient.to_dict()
    if 'hospitals' in obj:
        del obj['hospitals']
    if 'prescriptions' in obj:
        del obj['prescriptions']
    return jsonify(obj), 201


@app_views.route('/patients/<patient_id>', methods=['PUT'])
def update_patient(patient_id):
    '''Updates the patient with the given id.
    '''
    xkeys = ('id', 'email', 'created_at', 'updated_at')
    user = storage.get(Patient, patient_id)
    if patient:
        data = {}
        try:
            data = request.get_json()
        except Exception:
            data = None
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        for key, value in data.items():
            if key not in xkeys:
                setattr(patient, key, value)
        patient.save()
        obj = patient.to_dict()
        if 'hospitals' in obj:
            del obj['hospitals']
        if 'prescriptions' in obj:
            del obj['prescriptions']
        return jsonify(obj), 200
    raise NotFound()
