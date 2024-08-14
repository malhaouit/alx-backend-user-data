#!/usr/bin/env python3
""" Create a new Flask view that handles all routes for the session
authentication.
"""
from api.v1.views import app_views
from flask import jsonify, request, make_response
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ Handles session authentication login.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None or email == '':
        return jsonify({"error": "email missing"}), 400

    if password is None or password == '':
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({'email': email})
    except Exception:
        return jsonify({"error": "no user found for this email"}), 404

    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)
    session_name = os.getenv('SESSION_NAME')

    response = make_response(user.to_json())
    response.set_cookie(session_name, session_id)

    return response


@app_views.route(
        '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout():
    """ Handles logout request
    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
