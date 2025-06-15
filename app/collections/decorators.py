from functools import wraps

from flask import request
from flask_jwt_extended import get_jwt_identity

from app.collections.services.checks import (
    user_collection_exists, user_document_exists,
    document_in_collection_exists, user_collection_with_name_exists
)
from app.users.services import get_user_by_username


def ensure_user_collection_exists(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        collection_id = kwargs.get("collection_id")
        username = get_jwt_identity()
        user = get_user_by_username(username)

        if not user_collection_exists(user, collection_id):
            return {"message": "This user does not have such collection"}, 404
        return func(*args, **kwargs)
    return wrapper


def check_collection_not_exists(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        collection_name = request.json.get("collection_name")
        username = get_jwt_identity()
        user = get_user_by_username(username)

        if user_collection_with_name_exists(user, collection_name):
            return {"message": "Collection with this name already exists"}, 409

        return func(*args, **kwargs)
    return wrapper


def ensure_user_document_exists(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        document_id = kwargs.get("document_id")
        username = get_jwt_identity()
        user = get_user_by_username(username)

        if not user_document_exists(user, document_id):
            return {"message": "This user does not have such document"}, 404
        return func(*args, **kwargs)
    return wrapper


def ensure_document_not_in_collection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        collection_id = kwargs.get("collection_id")
        document_id = kwargs.get("document_id")

        if document_in_collection_exists(collection_id, document_id):
            return {
                "message": "This document already exists in this collection"
            }, 409
        return func(*args, **kwargs)
    return wrapper


def ensure_document_in_collection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        collection_id = kwargs.get("collection_id")
        document_id = kwargs.get("document_id")

        if not document_in_collection_exists(collection_id, document_id):
            return {
                "message": "This document is not part of this collection"
            }, 409
        return func(*args, **kwargs)

    return wrapper
