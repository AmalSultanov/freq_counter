from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource

from app.documents.api_models import (
    document_model, message_model, document_content_model, statistics_model,
    huffman_encoded_document_content_model
)
from app.documents.decorators import ensure_user_document_exists
from app.documents.error_handlers import register_documents_errors_handlers
from app.documents.namespace import api
from app.documents.selectors import (
    get_documents_by_username, fetch_document_contents,
    get_collections_idf_data, get_document_tf_cached
)
from app.documents.services.crud import remove_document, handle_document_upload
from app.documents.services.huffman import encode
from app.shared.file_utils import is_file_invalid

register_documents_errors_handlers(api)

upload_parser = api.parser()
upload_parser.add_argument(
    'file',
    location='files',
    type='FileStorage',
    required=True,
    help='A .txt file to upload (max size is 3 MB)'
)


class SecuredResource(Resource):
    method_decorators = [jwt_required()]


@api.route("")
class DocumentsListResource(SecuredResource):
    @api.doc(
        description="Get all documents for the current user",
        security="BearerAuth",
        responses={
            200: ("Documents were fetched", [document_model]),
            401: ("Missing JWT in headers or cookie", message_model),
        }
    )
    def get(self):
        """List documents for the current user"""
        username = get_jwt_identity()
        documents = get_documents_by_username(username)

        if not documents:
            return [], 200

        return [
            {"document_id": doc.id, "document_name": doc.name}
            for doc in documents
        ], 200

    @api.expect(upload_parser)
    @api.doc(
        description="Upload a new .txt document. "
                    "The size of it should not exceed 3 MB",
        security="BearerAuth",
        consumes=["multipart/form-data"],
        responses={
            201: ("Document was uploaded", message_model),
            400: ("Document is empty", message_model),
            401: ("Missing JWT in headers or cookie", message_model),
            409: ("Duplicate document is not allowed", message_model),
            413: ("Document is too large", message_model)
        }
    )
    def post(self):
        """Upload a document"""
        file = request.files.get("file")

        if is_file_invalid(file):
            return {"message": "Only .txt files are allowed"}, 400

        username = get_jwt_identity()
        document = handle_document_upload(file, username)

        return {
            "message": f"Document with id = {document.id} was uploaded"}, 201


@api.route("/<int:document_id>")
@api.param("document_id", "The document identifier")
class DocumentContentsResource(SecuredResource):
    @api.doc(
        description="Fetch document contents",
        security="BearerAuth",
        responses={
            200: ("Document was found", document_content_model),
            401: ("Missing JWT in headers or cookie", message_model),
            404: ("User does not have this document", message_model)
        }
    )
    @ensure_user_document_exists
    def get(self, document_id):
        """Get document contents"""
        document_data = fetch_document_contents(document_id)

        return {
            "document_id": document_id,
            "document_contents": document_data
        }, 200

    @api.doc(
        description="Delete a document by ID",
        security="BearerAuth",
        responses={
            200: ("Document deleted", message_model),
            401: ("Missing JWT in headers or cookie", message_model),
            404: ("User does not have this document", message_model)
        }
    )
    @ensure_user_document_exists
    def delete(self, document_id):
        """Delete a document"""
        username = get_jwt_identity()
        remove_document(username, document_id)

        return {"message": "Document was deleted"}, 200


@api.route("/<int:document_id>/huffman")
@api.param("document_id", "The document identifier")
class DocumentContentsHuffmanEncodedResource(SecuredResource):
    @api.doc(
        description="Fetch document contents and encode "
                    "into Huffman coding form",
        security="BearerAuth",
        responses={
            200: ("Document was encoded",
                  huffman_encoded_document_content_model),
            401: ("Missing JWT in headers or cookie", message_model),
            404: ("User does not have this document", message_model)
        }
    )
    @ensure_user_document_exists
    def get(self, document_id):
        """Get document contents in Huffman coding form"""
        document_data = fetch_document_contents(document_id)
        encoded_result, _ = encode(document_data)

        return {
            "document_id": document_id,
            "huffman_encoded_document_contents": encoded_result
        }, 200


@api.route("/<int:document_id>/statistics")
@api.param("document_id", "The document identifier")
class DocumentStatisticsResource(SecuredResource):
    @api.doc(
        description="Get TF-IDF statistics for a document if it belongs to "
                    "any collection, if not, get only TF stats with message "
                    "that document should be in at least 1 collection to get "
                    "IDF values",
        security="BearerAuth",
        responses={
            200: ("Document was found", statistics_model),
            401: ("Missing JWT in headers or cookie", message_model),
            404: ("User does not have this document", message_model)
        }
    )
    @ensure_user_document_exists
    def get(self, document_id):
        """Get TF-IDF statistics"""
        tf = get_document_tf_cached(document_id)
        collections_data = get_collections_idf_data(document_id, tf)

        if collections_data is None:
            msg = "Document is not part of any collection, IDF is unavailable"
            return {
                "document_id": document_id,
                "tf": tf,
                "message": msg
            }, 200

        return {
            "document_id": document_id,
            "collections_data": collections_data
        }, 200
