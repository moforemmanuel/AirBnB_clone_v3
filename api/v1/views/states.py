#!/usr/bin/python3
"""states"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route("/states", methods=['GET', 'POST'], strict_slashes=False)
def states():
    raw_states = storage.all('State')
    states_objs = [state_obj.to_dict() for state_obj in raw_states.values()]

    # get method
    if request.method == 'GET':
        return jsonify(states_objs)

    # post method
    if request.method == 'POST':
        if request.headers['Content-Type'] != 'application/json':
            abort(400, 'Not a JSON')
        else:
            body = request.get_json()
            if body.get('name') is None:
                abort(400, 'Missing name')
            else:
                print(body)
                new_state = State(**body)
                new_state.save()
                return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def state(state_id):
    state_instance = storage.get(State, state_id)
    if state_instance is None:
        abort(404)
    else:
        if request.method == 'GET':
            return jsonify(state_instance.to_dict())
        if request.method == 'DELETE':
            storage.delete(state_instance)
            return make_response(jsonify(), 200)
        if request.method == 'PUT':
            if request.headers['Content-Type'] != 'application/json':
                abort(400, 'Not a JSON')
            else:
                body = request.get_json()
                for key, value in body.items():
                    if key not in ('id', 'created_at', 'updated_at'):
                        setattr(state_instance, key, value)
            return make_response(jsonify(state_instance.to_dict()), 200)
