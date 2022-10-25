#!/usr/bin/python3
"""cities"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities",
                 methods=['GET', 'POST'], strict_slashes=False)
def cities(state_id):
    """router handler for cities get and post"""
    raw_cities = storage.all(City)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities_objs = [
        state_obj.to_dict()
        for state_obj in raw_cities.values()
        if state_obj.state_id == state_id
    ]

    # get method
    if request.method == 'GET':
        return jsonify(cities_objs)

    # post method
    if request.method == 'POST':
        if request.headers['Content-Type'] != 'application/json':
            abort(400, 'Not a JSON')
        else:
            body = request.get_json()
            if body.get('name') is None:
                abort(400, 'Missing name')
            else:
                # print(body)
                body['state_id'] = state_id
                new_city = City(**body)
                new_city.save()
                return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route("/cities/<city_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city(city_id):
    """router handler for city instance get, put and delete"""
    city_instance = storage.get(City, city_id)
    if city_instance is None:
        abort(404)
    else:
        if request.method == 'GET':
            return jsonify(city_instance.to_dict())
        if request.method == 'DELETE':
            storage.delete(city_instance)
            storage.save()
            return make_response(jsonify({}), 200)
        if request.method == 'PUT':
            if request.headers['Content-Type'] != 'application/json':
                abort(400, 'Not a JSON')
            else:
                body = request.get_json()
                for key, value in body.items():
                    if key not in ('id', 'created_at', 'updated_at'):
                        setattr(city_instance, key, value)
                storage.save()
            return make_response(jsonify(city_instance.to_dict()), 200)
