#!/usr/bin/python3
"""
This module creates an endpoint that retrieves
the number of each objects by type and returns the status of your API
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Returns the status of your API
    """
    status = {"status": "OK"}
    return jsonify(status)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
    Retrieves the number of each objects by type
    """
    stats = {
        "users": storage.count(User)}
    return jsonify(stats)
