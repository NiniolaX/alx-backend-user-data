#!/usr/bin/env python3
""" Basic Flask App """
from auth import Auth
from flask import Flask
from flask import jsonify, request, abort, make_response, redirect, url_for
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
        return jsonify({"message": "email not provided"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"message": "password not provided"}), 400

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
        return jsonify({"message": "email not provided"}), 400

    password = request.form.get('password')
    if not password:
        return jsonify({"message": "password not provided"}), 400

    # Validate user credentials
    if not AUTH.valid_login(email, password):
        abort(401)

    # Create session ID
    session_id = AUTH.create_session(email)

    # Create response object and store session ID as cookie
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """ For user logout """
    session_id = request.cookies.get('session_id')
    if session_id:
        # Get associated user
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            # Destroy user session
            AUTH.destroy_session(user.id)
            return redirect(url_for('home'))

    abort(403)  # User not found or invalid session


@app.route("/profile", strict_slashes=False)
def get_profile():
    """ Retrieves a user's profile """
    session_id = request.cookies.get('session_id')
    if session_id:
        # Get associated user
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email})

    abort(403)  # User not found or invalid session


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ Returns a user's reset password token """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email not provided"}), 400

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError:
        abort(403)


@app.route("/reset_password", methods=['PUT'], strict_slashes=False)
def update_password():
    """ Resets a user's password """
    email = request.form.get('email')
    if not email:
        return jsonify({"error": "email not provided"}), 400

    reset_token = request.form.get('reset_token')
    if not reset_token:
        return jsonify({"error": "reset token not provided"}), 400

    new_password = request.form.get('new_password')
    if not new_password:
        return jsonify({"error": "new password not provided"}), 400

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:  # If no user is associated with token or token invalid
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000", debug=True)
