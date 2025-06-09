from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request

from app.documents.decorators import ensure_user_document_exists
from app.documents.error_handlers import register_documents_errors_handlers
from app.documents.services import (
    get_documents_by_username, remove_document, get_document_tf, add_document,
    fetch_document_contents, get_collections_idf_data
)
from app.shared.file_utils import is_file_invalid

documents_api_bp = Blueprint("documents", __name__)
register_documents_errors_handlers(documents_api_bp)


@documents_api_bp.before_request
def require_jwt():
    verify_jwt_in_request()


@documents_api_bp.post("")
def upload_document():
    file = request.files.get("file")

    if is_file_invalid(file):
        return jsonify({"message": "Only .txt files are allowed"}), 400

    username = get_jwt_identity()
    document = add_document(file, username)

    return jsonify({
        "message": f"Document with id = {document.id} was uploaded"
    }), 201


@documents_api_bp.get("")
def get_user_documents():
    username = get_jwt_identity()
    documents = get_documents_by_username(username)

    if not documents:
        return jsonify([]), 200

    return jsonify([
        {"document_id": document.id, "document_name": document.name}
        for document in documents
    ]), 200


@documents_api_bp.get("/<int:document_id>")
@ensure_user_document_exists
def get_document_contents(document_id: int):
    document_data = fetch_document_contents(document_id)

    return jsonify({
        "document_id": document_data.id,
        "document_contents": document_data.contents
    }), 200


@documents_api_bp.get("/<int:document_id>/statistics")
@ensure_user_document_exists
def get_document_statistics(document_id: int):
    tf = get_document_tf(document_id)
    collections_data = get_collections_idf_data(document_id, tf)

    if collections_data is None:
        message = "Document is not part of any collection, IDF is unavailable"
        return jsonify({
            "document_id": document_id,
            "tf": tf,
            "message": message
        }), 200

    return jsonify({
        "document_id": document_id,
        "collections_data": collections_data
    }), 200


@documents_api_bp.delete("/<int:document_id>")
@ensure_user_document_exists
def delete_document(document_id: int):
    username = get_jwt_identity()
    remove_document(document_id, username)

    return jsonify({"message": f"Document was deleted"}), 200
