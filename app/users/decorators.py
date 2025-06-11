from functools import wraps

from flask_jwt_extended import get_jwt_identity

from app.users.services import get_user_by_username


def authorize_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = kwargs.get("user_id")
        username = get_jwt_identity()
        user = get_user_by_username(username)

        if user is None or user.id != user_id:
            return {
                "message": "You are not authorized to perform this action"
            }, 403
        return func(*args, **kwargs)

    return wrapper
