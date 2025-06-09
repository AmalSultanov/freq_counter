from flask import Blueprint, jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from app.collections.decorators import (
    ensure_user_collection_exists, ensure_user_document_exists,
    ensure_document_not_in_collection, ensure_document_in_collection
)
from app.collections.services import (
    get_collections_list, get_documents_by_collection_id, get_collection_stats,
    add_document_to_collection, delete_document_from_collection,
    add_collection
)

collections_api_bp = Blueprint("collections", __name__)


@collections_api_bp.before_request
def require_jwt():
    verify_jwt_in_request()


@collections_api_bp.post("")
def create_collection():
    username = get_jwt_identity()
    collection_name = request.json.get("collection_name")
    collection = add_collection(username, collection_name)

    return jsonify({
        "message": f"Collection with id = {collection.id} was created",
    }), 201


@collections_api_bp.get("")
def get_collections():
    username = get_jwt_identity()
    collections = get_collections_list(username)

    if not collections:
        return jsonify([]), 200

    result = []

    for collection in collections:
        documents = [{
            "document_id": document.document.id,
            "document_name": document.document.name}
            for document in collection.documents
        ]

        result.append({"collection_id": collection.id, "documents": documents})

    return jsonify(result), 200


@collections_api_bp.get("/<int:collection_id>")
@ensure_user_collection_exists
def get_documents_by_collection(collection_id: int):
    documents = get_documents_by_collection_id(collection_id)
    document_ids = [document.document_id for document in documents]

    return jsonify({"document_ids": document_ids}), 200


@collections_api_bp.get("/<int:collection_id>/statistics")
@ensure_user_collection_exists
def get_collection_statistics(collection_id: int):
    tf, idf = get_collection_stats(collection_id)
    response = {"collection_id": collection_id, "tf": tf, "idf": idf}

    if not tf:
        response["message"] = "No documents in collection were found"

    return jsonify(response), 200


@collections_api_bp.post("/<int:collection_id>/<int:document_id>")
@ensure_user_collection_exists
@ensure_user_document_exists
@ensure_document_not_in_collection
def add_document(collection_id: int, document_id: int):
    add_document_to_collection(collection_id, document_id)
    return jsonify({"message": "Document was added to collection"}), 201


@collections_api_bp.delete("/<int:collection_id>/<int:document_id>")
@ensure_user_collection_exists
@ensure_user_document_exists
@ensure_document_in_collection
def delete_document(collection_id: int, document_id: int):
    delete_document_from_collection(collection_id, document_id)
    return jsonify({
        "message": "Document was deleted from this collection"
    }), 200
