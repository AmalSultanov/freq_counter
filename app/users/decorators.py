from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from app.users.services import get_user_by_username


def authorize_user(func):
    @wraps(func)
    def wrapper(user_id, *args, **kwargs):
        username = get_jwt_identity()
        user = get_user_by_username(username)

        if user is None or user.id != user_id:
            return jsonify({
                "message": "You are not authorized to perform this action"
            }), 403
        return func(user_id, *args, **kwargs)

    return wrapper
