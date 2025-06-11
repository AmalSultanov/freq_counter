from functools import wraps

from flask_jwt_extended import get_jwt_identity

from app.documents.services import user_has_document
from app.users.services import get_user_by_username


def ensure_user_document_exists(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        document_id = kwargs.get("document_id")
        username = get_jwt_identity()
        user = get_user_by_username(username)

        if not user_has_document(document_id, user):
            return {"message": "This user does not have such document"}, 404
        return func(*args, **kwargs)
    return wrapper
