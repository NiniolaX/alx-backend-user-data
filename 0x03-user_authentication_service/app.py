#!/usr/bin/env python3
""" Basic Flask App """
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", strict_slashes=False)
def home():
    """ Home route """
    return jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
