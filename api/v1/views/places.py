#!/usr/bin/python3
"""places"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place


@app_views.route("/cities/<city_id>/places",
                 methods=['GET', 'POST'], strict_slashes=False)
def places_r(city_id):
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
def place_r(place_id):
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


# @app_views.route('/places_search', methods=['POST'])
# def places_search():
#     """Retrieve all place objects based on json req"""
#     if request.headers['Content-Type'] != 'application/json':
#         abort(400, 'Not a JSON')
#
#     body = request.get_json()
#     if (not body) or (not body['states'] and
#          not body['cities'] and
#          not body['amenities']):
#         # print(storage.all('Place'))
#         return jsonify([x.to_dict() for x in storage.all('Place').values()])
#
#     if body['states']:
#         # return jsonify([
#         #     x.to_dict() for x in storage.all('Place').values()
#         #     if storage.get('City', x.city_id).state_id == state_id
#         #        for state_id in body['states']
#         # ])
#
#         place_objs = []
#         for place_obj in storage.all('Place').values():
#             for state_id in body['states']:
#                 if storage.get('City', place_obj.city_id).state_id == state_id:
#                     place_objs.append(place_obj.to_dict())
#
#         return jsonify(place_objs)

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """searches for a place"""
    if request.get_json() is not None:
        params = request.get_json()
        states = params.get('states', [])
        cities = params.get('cities', [])
        amenities = params.get('amenities', [])
        amenity_objects = []
        for amenity_id in amenities:
            amenity = storage.get('Amenity', amenity_id)
            if amenity:
                amenity_objects.append(amenity)
        if states == cities == []:
            places = storage.all('Place').values()
        else:
            places = []
            for state_id in states:
                state = storage.get('State', state_id)
                state_cities = state.cities
                for city in state_cities:
                    if city.id not in cities:
                        cities.append(city.id)
            for city_id in cities:
                city = storage.get('City', city_id)
                for place in city.places:
                    places.append(place)
        confirmed_places = []
        for place in places:
            place_amenities = place.amenities
            confirmed_places.append(place.to_dict())
            for amenity in amenity_objects:
                if amenity not in place_amenities:
                    confirmed_places.pop()
                    break
        return jsonify(confirmed_places)
    else:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
