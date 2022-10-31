#!/usr/bin/python3
"""places_amenities"""
import os
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage


@app_views.route('/places/<string:place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_place_amenities(place_id):
    """get amenity information for a specified place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    amenities = []
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        amenity_objects = place.amenities
    else:
        amenity_objects = place.amenity_ids
    for amenity in amenity_objects:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """deletes an amenity object from a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity not in place_amenities:
        abort(404)
    place_amenities.remove(amenity)
    place.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['POST'], strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """adds an amenity object to a place"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        place_amenities = place.amenities
    else:
        place_amenities = place.amenity_ids
    if amenity in place_amenities:
        return jsonify(amenity.to_dict())
    place_amenities.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)

# #!/usr/bin/python3
# """places_amenities"""
# import models
# from api.v1.views import app_views
# from flask import jsonify, abort, request, make_response
# from models import storage
# from models.amenity import Amenity
#
#
# @app_views.route("/places/<place_id>/amenities",
#                  methods=['GET'], strict_slashes=False)
# def amenities_of_place(place_id):
#     """router handler for cities get and post"""
#     raw_amenities = storage.all(Amenity)
#     place = storage.get('Place', place_id)
#     if place is None:
#         abort(404)
#     amenity_objs = []
#     if models.storage_t == 'db':
#         amenity_objs = [
#             amenity_obj.to_dict()
#             for amenity_obj in raw_amenities.values()
#             if amenity_obj.place_id == place_id
#         ]
#
#     else:
#         amenity_ids = place.amenity_list
#         amenity_objs = [
#             amenity_obj.to_dict()
#             for amenity_obj in list(map(
#                 lambda amenity_id: models.storage.get(Amenity, amenity_id),
#                 amenity_ids))
#         ]
#
#     # get method
#     if request.method == 'GET':
#         return jsonify(amenity_objs)
#
#
# @app_views.route("/places/<place_id>/amenities/<amenity_id>", methods=['DELETE', 'POST'],
#                  strict_slashes=False)
# def amenity_of_place(place_id, amenity_id):
#     """router handler for city instance get, put and delete"""
#     place = storage.get('Place', place_id)
#     amenity = storage.get(Amenity, amenity_id)
#     if place is None:
#         abort(404)
#     if (amenity is None) or (amenity.place_id != place.id):
#         abort(404)
#     else:
#         if request.method == 'DELETE':
#             if models.storage_t == 'db':
#                 storage.delete(amenity)
#                 storage.save()
#             else:
#                 place.amenity_list.remove(amenity.id)
#                 storage.save()
#             return make_response(jsonify({}), 200)
#
#         if request.method == 'POST':
#             if hasattr(amenity, 'place_id'):
#                 return make_response(jsonify(amenity.to_dict()), 200)
#             return make_response(jsonify(amenity.to_dict()), 200)
