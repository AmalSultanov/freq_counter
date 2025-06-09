from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from app.documents.services import (
    user_has_document
)
from app.users.services import get_user_by_username


def ensure_user_document_exists(func):
    @wraps(func)
    def wrapper(document_id, *args, **kwargs):
        username = get_jwt_identity()
        user = get_user_by_username(username)

        if not user_has_document(document_id, user):
            return jsonify({
                "message": "This user does not have such document"
            }), 404
        return func(document_id, *args, **kwargs)

    return wrapper
