from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity

from app.collections.services import (
    user_collection_exists, user_document_exists, document_in_collection_exists
)
from app.users.services import get_user_by_username


def ensure_user_collection_exists(func):
    @wraps(func)
    def wrapper(collection_id, *args, **kwargs):
        username = get_jwt_identity()
        user = get_user_by_username(username)

        if not user_collection_exists(collection_id, user):
            return jsonify({
                "message": "This user does not have such collection"
            }), 404
        return func(collection_id, *args, **kwargs)

    return wrapper


def ensure_user_document_exists(func):
    @wraps(func)
    def wrapper(collection_id, document_id, *args, **kwargs):
        username = get_jwt_identity()
        user = get_user_by_username(username)

        if not user_document_exists(document_id, user):
            return jsonify({
                "message": "This user does not have such document"
            }), 404
        return func(collection_id, document_id, *args, **kwargs)

    return wrapper


def ensure_document_not_in_collection(func):
    @wraps(func)
    def wrapper(collection_id, document_id, *args, **kwargs):
        if document_in_collection_exists(collection_id, document_id):
            return jsonify({
                "message": "This document already exists in this collection"
            }), 409
        return func(collection_id, document_id, *args, **kwargs)

    return wrapper


def ensure_document_in_collection(func):
    @wraps(func)
    def wrapper(collection_id, document_id, *args, **kwargs):
        if not document_in_collection_exists(collection_id, document_id):
            return jsonify({
                "message": "This document is not part of this collection"
            }), 409
        return func(collection_id, document_id, *args, **kwargs)

    return wrapper
