from flask import request, make_response
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies
)
from flask_restx import Resource

from app.users.api_models import (
    login_model, token_response, message_response, register_model,
    password_update_model
)
from app.users.decorators import authorize_user
from app.users.namespace import api
from app.users.services import (
    authenticate_user, generate_tokens, register_user, change_user_password,
    remove_user
)


@api.route("/login")
class LoginResource(Resource):
    @api.doc(
        description="Authenticate user and return access token",
        security=[],
        responses={
            201: ("Login was successful", token_response),
            401: ("Invalid credentials", message_response)
        }
    )
    @api.expect(login_model)
    def post(self):
        """Log in a user"""
        data = request.json
        result = authenticate_user(data["username"], data["password"])

        if "message" in result:
            return {"message": result["message"]}, 401

        response = {"message": "Login was successful",
                    "access_token": result["access_token"]}
        response = make_response(response, 201)

        set_access_cookies(response, result["access_token"])
        set_refresh_cookies(response, result["refresh_token"])

        return response


@api.route("/register")
class RegisterResource(Resource):
    @api.doc(
        description="Register a new user and set tokens",
        security=[],
        responses={
            201: ("User created", token_response),
            409: ("User already exists", message_response),
        }
    )
    @api.expect(register_model)
    def post(self):
        """Register a new user"""
        data = request.json
        user = register_user(data["username"], data["password"])

        if not user:
            return {"message": "User with this username already exists"}, 409

        tokens = generate_tokens(data["username"])
        response = {
            "message": f"User with id = {user.id} was created",
            "access_token": tokens["access_token"]
        }
        response = make_response(response, 201)

        set_access_cookies(response, tokens["access_token"])
        set_refresh_cookies(response, tokens["refresh_token"])

        return response


@api.route("/logout")
class LogoutResource(Resource):
    @jwt_required()
    @api.doc(
        description="Logout the current user by unsetting JWT cookies",
        security="BearerAuth",
        responses={
            200: ("Logout successful", message_response),
            401: ("Missing JWT in headers or cookie", message_response)
        }
    )
    def get(self):
        """Log out the current user"""
        response = make_response({
            "message": "Logout was successful"
        }, 200)
        unset_jwt_cookies(response)

        return response


@api.route("/<int:user_id>")
class UserResource(Resource):
    @jwt_required()
    @authorize_user
    @api.doc(
        description="Update the password for the authenticated user. "
                    "**Note:** Clients must send the `csrf_access_token` "
                    "cookie value in the `X-CSRF-TOKEN` header every time "
                    "they call this endpoint",
        security="BearerAuth",
        responses={
            200: ("Password updated", message_response),
            400: ("Same password", message_response),
            401: ("Missing JWT in headers or cookie", message_response),
            403: ("User is not authorized to perform this action",
                  message_response)
        }
    )
    @api.expect(password_update_model)
    def patch(self, user_id):
        """Update the password for the authenticated user"""
        new_password = request.json.get("password")
        result = change_user_password(user_id, new_password)

        if result is None:
            return {"message": "Password is the same as before"}, 400

        response = make_response({
            "message": "Password was updated. Tokens refreshed."
        }, 200)
        username = get_jwt_identity()
        tokens = generate_tokens(username)
        set_access_cookies(response, tokens["access_token"])

        return response

    @jwt_required()
    @authorize_user
    @api.doc(
        description="Delete the authenticated user and clear cookies. "
                    "**Note:** Clients must send the `csrf_access_token` "
                    "cookie value in the `X-CSRF-TOKEN` header every time "
                    "they call this endpoint",
        security="BearerAuth",
        responses={
            200: ("User was deleted", message_response),
            401: ("Missing JWT in headers or cookie", message_response),
            403: ("User is not authorized to perform this action",
                  message_response)
        }
    )
    def delete(self, user_id):
        """Delete the authenticated user"""
        user = remove_user(user_id)
        response = make_response(
            {"message": f"User '{user.username}' was deleted"}, 200
        )
        unset_jwt_cookies(response)

        return response


@api.route("/refresh")
class RefreshResource(Resource):
    @jwt_required(refresh=True)
    @api.doc(
        description="Use refresh token to obtain a new access token. "
                    "**Note:** Clients must send the `csrf_refresh_token` "
                    "cookie value in the `X-CSRF-TOKEN` header every time "
                    "they call this endpoint",
        security="BearerAuth",
        responses={
            200: ("Token refreshed", message_response),
            401: ("Missing JWT in headers or cookie", message_response),
            422: ("Unprocessable entity", message_response)
        }
    )
    def post(self):
        """Refresh the access token"""
        username = get_jwt_identity()
        tokens = generate_tokens(username)
        response = make_response({
            "message": "Access token was refreshed"
        }, 200)
        set_access_cookies(response, tokens["access_token"])

        return response
