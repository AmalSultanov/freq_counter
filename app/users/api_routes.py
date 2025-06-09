from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies
)

from app.users.decorators import authorize_user
from app.users.services import (
    authenticate_user, generate_tokens, register_user, change_user_password,
    remove_user
)

users_api_bp = Blueprint("users", __name__)


@users_api_bp.post("/login")
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    result = authenticate_user(username, password)

    if "message" in result:
        return jsonify({"message": result.get("message")}), 401

    response = jsonify({"message": "Login was successful"})
    set_access_cookies(response, result["access_token"])
    set_refresh_cookies(response, result["refresh_token"])

    return response, 201


@users_api_bp.post("/register")
def register():
    username = request.json.get("username")
    password = request.json.get("password")
    user = register_user(username, password)

    if not user:
        return jsonify({
            "message": "User with this username already exists"
        }), 409

    tokens = generate_tokens(username)
    response = jsonify({"message": f"User with id = {user.id} was created"})
    set_access_cookies(response, tokens["access_token"])
    set_refresh_cookies(response, tokens["refresh_token"])
    return response, 201


@users_api_bp.get("/logout")
@jwt_required()
def logout():
    response = jsonify({"message": "Logout was successful"})
    unset_jwt_cookies(response)

    return response, 200


@users_api_bp.patch("/<int:user_id>")
@jwt_required()
@authorize_user
def update_password(user_id):
    new_password = request.json.get("password")
    result = change_user_password(user_id, new_password)

    if result is None:
        return jsonify({"message": "Password is the same as before"}), 400

    return jsonify({"message": "Password was updated successfully"}), 200


@users_api_bp.delete("/<int:user_id>")
@jwt_required()
@authorize_user
def delete_user(user_id):
    user = remove_user(user_id)
    response = jsonify({
        "message": f"User '{user.username}' was deleted"
    })
    unset_jwt_cookies(response)

    return response, 200


@users_api_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    username = get_jwt_identity()
    tokens = generate_tokens(username)
    response = jsonify({"message": "Access token was refreshed"})
    set_access_cookies(response, tokens["access_token"])

    return response, 200
