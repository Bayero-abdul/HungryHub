#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML
"""
from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from flask_cors import CORS
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
CORS(app)
app.register_blueprint(app_views)
app.config["JWT_SECRET_KEY"] = "afdasfafafjk35423452345klnvsnkfasf"
jwt = JWTManager(app)


@app.teardown_appcontext
def close_storage(exception):
    """
    method to close the storage after each request
    """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """
    Handler for 404 errors that returns a JSON-formatted 404 status error
    """
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = os.environ.get('HUB_API_HOST', '0.0.0.0')
    port = os.environ.get('HUB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
