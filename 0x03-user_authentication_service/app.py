#!/usr/bin/env python3
""" Basic Flask App """
from auth import Auth
from flask import Flask, jsonify, request, abort, make_response
from flask_cors import CORS

AUTH = Auth()

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", strict_slashes=False)
def home():
    """ Home route """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """ For user registration """
    email = request.form.get('email')
    if not email:
        return jsonify({"message": "No email provided"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"message": "No password provided"}), 400

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """ For user login """
    email = request.form.get('email')
    if not email:
        return jsonify({"message": "No email provided"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"message": "No password provided"}), 400

    # Validate user credentials
    if not AUTH.valid_login(email, password):
        abort(401)

    # Create session ID
    session_id = AUTH.create_session(email)

    # Create response object and store session ID as cookie
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
