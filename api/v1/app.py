#!/usr/bin/python3
"""Start of API"""

from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def not_found(self):
    """Not found handler"""
    return jsonify(error="Not found")


@app.teardown_appcontext
def teardown(self):
    """close session storage"""
    storage.close()


if __name__ == '__main__':
    app.run(
        host=getenv('HBNB_API_HOST', default='0.0.0.0'),
        port=getenv('HBNB_API_PORT', default=5000),
        threaded=True
    )
