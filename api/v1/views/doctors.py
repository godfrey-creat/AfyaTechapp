#!/usr/bin/python3
'''Contains the doctors view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, BadRequest

from api.v1.views import app_views
from models import storage
from models.doctor import Doctor


@app_views.route('/doctors', methods=['GET'])
@app_views.route('/doctors/<doctor_id>', methods=['GET'])
def get_doctors(doctor_id=None):
    '''Gets the doctor with the given id or all doctors.
    '''
    if doctor_id:
        doctor = storage.get(Doctor, doctor_id)
        if doctor:
            obj = doctor.to_dict()
            if 'patients' in obj:
                del obj['patients']
            if 'prescriptions' in obj:
                del obj['prescriptions']
            return jsonify(obj)
        raise NotFound()
    all_doctors = storage.all(Doctor).values()
    doctors = []
    for doctor in all_doctors:
        obj = doctor.to_dict()
        if 'patients' in obj:
            del obj['patients']
        if 'prescriptions' in obj:
            del obj['prescriptions']
        doctors.append(obj)
    return jsonify(doctors)


@app_views.route('/doctors/<doctor_id>', methods=['DELETE'])
def remove_doctor(doctor_id):
    '''Removes a doctor with the given id.
    '''
    doctor = storage.get(Doctor, doctor_id)
    if doctor:
        storage.delete(doctor)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


@app_views.route('/doctors', methods=['POST'])
def add_doctor():
    '''Adds a new doctor.
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
    doctor = Doctor(**data)
    doctor.save()
    obj = doctor.to_dict()
    if 'patients' in obj:
        del obj['patients']
    if 'prescriptions' in obj:
        del obj['prescriptions']
    return jsonify(obj), 201


@app_views.route('/doctors/<doctor_id>', methods=['PUT'])
def update_doctor(doctor_id):
    '''Updates the doctor with the given id.
    '''
    xkeys = ('id', 'email', 'created_at', 'updated_at')
    doctor = storage.get(Doctor, doctor_id)
    if doctor:
        data = {}
        try:
            data = request.get_json()
        except Exception:
            data = None
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        for key, value in data.items():
            if key not in xkeys:
                setattr(doctor, key, value)
        doctor.save()
        obj = doctor.to_dict()
        if 'patients' in obj:
            del obj['patients']
        if 'prescriptions' in obj:
            del obj['prescriptions']
        return jsonify(obj), 200
    raise NotFound()
