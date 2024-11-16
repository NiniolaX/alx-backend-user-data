#!/usr/bin/env python3
"""
Handles all routes for session authentication
"""
from api.v1.app import app_views
from flask import abort, jsonify, make_response, request
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ Logs in a user """
    # Extract user email
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email missing"}), 400

    # Extract user password
    password = request.form.get('password')
    if not password:
        return jsonify({"error": "password missing"}), 400

    # Retrieve and validate user based on provided email and password
    users = User.search({"email": email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]  # Assumed emails were unique and extracted first match

    # Validate user password
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    # Create Session ID for user
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = make_response(jsonify(user.to_json()))
    session_name = getenv('SESSION_NAME')
    response.set_cookie(session_name, session_id)

    return response


@app_views.route('auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ Logs out a user """
    from api.v1.app import auth

    destroy_session_result = auth.destroy_session(request)
    if not destroy_session_result:
        abort(404)

    return jsonify({}), 200
