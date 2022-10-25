#!/usr/bin/python3
"""amenities"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=['GET', 'POST'],
                 strict_slashes=False)
def amenities():
    """router handler for amenities get and post"""
    raw_amenities = storage.all(Amenity)
    amenity_objs = [
        amenity_obj.to_dict()
        for amenity_obj in raw_amenities.values()
    ]

    # get method
    if request.method == 'GET':
        return jsonify(amenity_objs)

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
                new_amenity = Amenity(**body)
                new_amenity.save()
                return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenity(amenity_id):
    """router handler for amenity instance get, put and delete"""
    amenity_instance = storage.get(Amenity, amenity_id)
    if amenity_instance is None:
        abort(404)
    else:
        if request.method == 'GET':
            return jsonify(amenity_instance.to_dict())
        if request.method == 'DELETE':
            storage.delete(amenity_instance)
            storage.save()
            return make_response(jsonify({}), 200)
        if request.method == 'PUT':
            if request.headers['Content-Type'] != 'application/json':
                abort(400, 'Not a JSON')
            else:
                body = request.get_json()
                for key, value in body.items():
                    if key not in ('id', 'created_at', 'updated_at'):
                        setattr(amenity_instance, key, value)
                storage.save()
            return make_response(jsonify(amenity_instance.to_dict()), 200)
