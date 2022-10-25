#!/usr/bin/python3
"""states"""

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage


@app_views.route("/states", methods=['GET'])
def states():
    raw_states = storage.all('State')
    states_objs = [state_obj.to_dict() for state_obj in raw_states.values()]
    return jsonify(states_objs)


@app_views.route("/states/<state_id>", methods=['GET', 'DELETE', 'POST', 'PUT'])
def state(state_id):
    raw_states = storage.all('State')
    state_obj = None
    for key, value in raw_states.items():
        if state_id == key.split('.')[1]:
            state_obj = value.to_dict()
            break
    if state_obj is None:
        abort(404)
    return jsonify(state_obj)
