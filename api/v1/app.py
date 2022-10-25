#!/usr/bin/python3
"""Start of API"""

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(error):
    """Not found handler"""
    return make_response(jsonify(error="Not found"), 404)


@app.teardown_appcontext
def teardown(self):
    """close session storage"""
    storage.close()


if __name__ == '__main__':
    app.run(
        host=getenv('HBNB_API_HOST', default='0.0.0.0'),
        port=getenv('HBNB_API_PORT', default=5000),
        threaded=True,
        debug=True
    )
