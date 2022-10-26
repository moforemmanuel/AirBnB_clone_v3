#!/usr/bin/python3
"""reviews"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews",
                 methods=['GET', 'POST'], strict_slashes=False)
def reviews(place_id):
    """router handler for cities get and post"""
    raw_reviews = storage.all('Review')
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    review_objs = [
        review_obj.to_dict()
        for review_obj in raw_reviews.values()
        if review_obj.place_id == place_id
    ]

    # get method
    if request.method == 'GET':
        return jsonify(review_objs)

    # post method
    if request.method == 'POST':
        if request.headers['Content-Type'] != 'application/json':
            abort(400, 'Not a JSON')
        else:
            body = request.get_json()
            if body.get('user_id') is None:
                abort(400, 'Missing user_id')
            elif body.get('test') is None:
                abort(400, 'Missing text')
            else:
                # print(body)
                body['place_id'] = place_id
                new_review = Review(**body)
                new_review.save()
                return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def review(review_id):
    """router handler for city instance get, put and delete"""
    review_instance = storage.get(Review, review_id)
    if review_instance is None:
        abort(404)
    else:
        if request.method == 'GET':
            return jsonify(review_instance.to_dict())
        if request.method == 'DELETE':
            storage.delete(review_instance)
            storage.save()
            return make_response(jsonify({}), 200)
        if request.method == 'PUT':
            if request.headers['Content-Type'] != 'application/json':
                abort(400, 'Not a JSON')
            else:
                body = request.get_json()
                for key, value in body.items():
                    if key not in ('id', 'created_at', 'updated_at',
                                   'place_id'):
                        setattr(review_instance, key, value)
                storage.save()
            return make_response(jsonify(review_instance.to_dict()), 200)
