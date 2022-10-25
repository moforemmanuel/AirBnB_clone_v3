#!/usr/bin/python3
"""users"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route("/users", methods=['GET', 'POST'], strict_slashes=False)
def users():
    """router handler for users get and post"""
    raw_users = storage.all(User)
    user_objs = [user_obj.to_dict() for user_obj in raw_users.values()]

    # get method
    if request.method == 'GET':
        return jsonify(user_objs)

    # post method
    if request.method == 'POST':
        if request.headers['Content-Type'] != 'application/json':
            abort(400, 'Not a JSON')
        else:
            body = request.get_json()
            if body.get('email') is None:
                abort(400, 'Missing email')
            elif body.get('password') is None:
                abort(400, 'Missing password')
            else:
                # print(body)
                new_user = User(**body)
                new_user.save()
                return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def user(user_id):
    """router handler for user instance get, put and delete"""
    user_instance = storage.get(User, user_id)
    if user_instance is None:
        abort(404)
    else:
        if request.method == 'GET':
            return jsonify(user_instance.to_dict())
        if request.method == 'DELETE':
            storage.delete(user_instance)
            storage.save()
            return make_response(jsonify({}), 200)
        if request.method == 'PUT':
            if request.headers['Content-Type'] != 'application/json':
                abort(400, 'Not a JSON')
            else:
                body = request.get_json()
                for key, value in body.items():
                    if key not in ('id', 'created_at', 'updated_at'):
                        setattr(user_instance, key, value)
                storage.save()
            return make_response(jsonify(user_instance.to_dict()), 200)
