#!/usr/bin/python3
'''Contains the hospitals view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.hospital import Hospital


ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
'''Methods allowed for the hospitals endpoint.'''


@app_views.route('/hospitals', methods=ALLOWED_METHODS)
@app_views.route('/hospitals/<hospital_id>', methods=ALLOWED_METHODS)
def handle_hospitals(hospital_id=None):
    '''The method handler for the hospitals endpoint.
    '''
    handlers = {
        'GET': get_hospitals,
        'DELETE': remove_hospital,
        'POST': add_hospital,
        'PUT': update_hospital,
    }
    if request.method in handlers:
        return handlers[request.method](hospital_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_hospitals(hospital_id=None):
    '''Gets the hospital with the given id or all hospitals.
    '''
    all_hospitals = storage.all(Hospital).values()
    if hospital_id:
        res = list(filter(lambda x: x.id == hospital_id, all_hospitals))
        if res:
            return jsonify(res[0].to_dict())
        raise NotFound()
    all_hospitals = list(map(lambda x: x.to_dict(), all_hospitals))
    return jsonify(all_hospitals)


def remove_hospital(hospital_id=None):
    '''Removes a hospital with the given id.
    '''
    all_hospitals = storage.all(Hospital).values()
    res = list(filter(lambda x: x.id == hospital_id, all_hospitals))
    if res:
        storage.delete(res[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_hospital(hospital_id=None):
    '''Adds a new hospital.
    '''
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_hospital = Hospital(**data)
    new_hospital.save()
    return jsonify(new_hospital.to_dict()), 201


def update_hospital(hospital_id=None):
    '''Updates the hospital with the given id.
    '''
    xkeys = ('id', 'created_at', 'updated_at')
    all_hospitals = storage.all(Hospital).values()
    res = list(filter(lambda x: x.id == hospital_id, all_hospitals))
    if res:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        old_hospital = res[0]
        for key, value in data.items():
            if key not in xkeys:
                setattr(old_hospital, key, value)
        old_hospital.save()
        return jsonify(old_hospital.to_dict()), 200
    raise NotFound()
