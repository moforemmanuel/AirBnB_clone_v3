#!/usr/bin/python3
"""places"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place


@app_views.route("/cities/<city_id>/places",
                 methods=['GET', 'POST'], strict_slashes=False)
def places(city_id):
    """router handler for places get and post"""
    raw_places = storage.all(Place)
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    place_objs = [
        place_obj.to_dict()
        for place_obj in raw_places.values()
        if place_obj.city_id == city_id
    ]

    # get method
    if request.method == 'GET':
        return jsonify(place_objs)

    # post method
    if request.method == 'POST':
        if request.headers['Content-Type'] != 'application/json':
            abort(400, 'Not a JSON')
        else:
            body = request.get_json()
            if body.get('user_id') is None:
                abort(400, 'Missing user_id')
            elif body.get('name') is None:
                abort(400, 'Missing name')
            else:
                if storage.get('User', body.get('user_id')) is None:
                    abort(404)
                body['city_id'] = city_id
                new_place = Place(**body)
                new_place.save()
                return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place(place_id):
    """router handler for place instance get, put and delete"""
    place_instance = storage.get(Place, place_id)
    if place_instance is None:
        abort(404)
    else:
        if request.method == 'GET':
            return jsonify(place_instance.to_dict())
        if request.method == 'DELETE':
            storage.delete(place_instance)
            storage.save()
            return make_response(jsonify({}), 200)
        if request.method == 'PUT':
            if request.headers['Content-Type'] != 'application/json':
                abort(400, 'Not a JSON')
            else:
                body = request.get_json()
                for key, value in body.items():
                    if key not in ('id', 'created_at', 'updated_at',
                                   'city_id', 'user_id'):
                        setattr(place_instance, key, value)
                storage.save()
            return make_response(jsonify(place_instance.to_dict()), 200)
