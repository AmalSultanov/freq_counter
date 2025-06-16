from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Resource, fields

from app.collections.api_models import (
    collection_response, collection_input, message_model, statistics_response
)
from app.collections.decorators import (
    ensure_user_collection_exists, ensure_user_document_exists,
    ensure_document_not_in_collection, ensure_document_in_collection,
    check_collection_not_exists
)
from app.collections.namespace import api
from app.collections.selectors import (
    get_collections_list, get_documents_by_collection_id, get_collection_stats
)
from app.collections.services.crud import (
    add_document_to_collection, delete_document_from_collection,
    add_collection, remove_collection, update_collection_name
)


class SecuredResource(Resource):
    method_decorators = [jwt_required()]


@api.route("")
class CollectionListResource(SecuredResource):
    @api.doc(
        description="Get list of user collections and documents in them",
        security="BearerAuth",
        responses={
            200: ("Success", [collection_response]),
            401: ("Missing JWT in headers or cookie", message_model)
        }
    )
    def get(self):
        """List current user's collections with documents in them"""
        username = get_jwt_identity()
        collections = get_collections_list(username)

        if not collections:
            return [], 200

        result = []
        for collection in collections:
            documents = [{
                "document_id": document.document.id,
                "document_name": document.document.name}
                for document in collection.documents
            ]
            result.append(
                {"collection_id": collection.id, "documents": documents}
            )

        return result, 200

    @api.doc(
        description="Create a new collection",
        security="BearerAuth",
        responses={
            201: ("Collection created", message_model),
            401: ("Missing JWT in headers or cookie", message_model),
            409: ("Collection with this name already exists", message_model)
        }
    )
    @api.expect(collection_input)
    @check_collection_not_exists
    def post(self):
        """Create a new collection"""
        username = get_jwt_identity()
        collection_name = request.json.get("collection_name")
        collection = add_collection(username, collection_name)

        return {
            "message": f"Collection with id = {collection.id} was created"
        }, 201


@api.route("/<int:collection_id>")
@api.param("collection_id", "The collection identifier")
class CollectionDocumentsResource(SecuredResource):
    @api.doc(
        description="Get document IDs in a collection",
        security="BearerAuth",
        responses={
            200: ("Success", fields.List(fields.Integer)),
            401: ("Missing JWT in headers or cookie", message_model)
        }
    )
    @ensure_user_collection_exists
    def get(self, collection_id):
        """Get documents in collection"""
        documents = get_documents_by_collection_id(collection_id)
        document_ids = [document.document_id for document in documents]

        return {"document_ids": document_ids}, 200

    @api.doc(
        description="Update the name of particular collection",
        security="BearerAuth",
        responses={
            200: ("Collection was removed", message_model),
            401: ("Missing JWT in headers or cookie", message_model),
            404: ("User does not have such collection", message_model),
        }
    )
    @api.expect(collection_input)
    @ensure_user_collection_exists
    def patch(self, collection_id):
        """Update collection name"""
        username = get_jwt_identity()
        collection_name = request.json.get("collection_name")
        update_collection_name(username, collection_id, collection_name)

        return {"message": f"Collection was updated"}, 201

    @api.doc(
        description="Delete a collection, documents in it will be "
                    "unlinked from this collection but not deleted",
        security="BearerAuth",
        responses={
            200: ("Collection was removed", message_model),
            401: ("Missing JWT in headers or cookie", message_model),
            404: ("User does not have such collection", message_model),
        }
    )
    @ensure_user_collection_exists
    def delete(self, collection_id):
        """Delete collection"""
        username = get_jwt_identity()
        remove_collection(username, collection_id)

        return {"message": "Collection was deleted"}, 200


@api.route("/<int:collection_id>/statistics")
@api.param("collection_id", "The collection identifier")
class CollectionStatisticsResource(SecuredResource):
    @api.doc(
        description="Get TF-IDF statistics for a collection",
        security="BearerAuth",
        responses={
            200: ("Success", statistics_response),
            401: ("Missing JWT in headers or cookie", message_model),
        }
    )
    @ensure_user_collection_exists
    def get(self, collection_id):
        """Get collection TF-IDF statistics"""
        number_of_documents, tf, idf = get_collection_stats(collection_id)
        response = {"collection_id": collection_id}

        if number_of_documents == 0:
            response["message"] = "No documents in collection were found"
        elif number_of_documents == 1:
            response["tf"] = tf
            response["message"] = ("There is only one document in this "
                                   "collection, IDF is unavailable")
        else:
            response["idf"] = idf

        return response, 200


@api.route("/<int:collection_id>/<int:document_id>")
@api.param("collection_id", "The collection identifier")
@api.param("document_id", "The document identifier")
class CollectionDocumentResource(SecuredResource):
    @api.doc(
        description="Add a document to a collection",
        security="BearerAuth",
        responses={
            201: ("Document added", message_model),
            401: ("Missing JWT in headers or cookie", message_model),
            404: ("User does not have such collection or document",
                  message_model),
            409: ("Document already exists in this collection", message_model),
        }
    )
    @ensure_user_collection_exists
    @ensure_user_document_exists
    @ensure_document_not_in_collection
    def post(self, collection_id, document_id):
        """Add document to collection"""
        add_document_to_collection(collection_id, document_id)
        return {"message": "Document was added to collection"}, 201

    @api.doc(
        description="Remove a document from a collection",
        security="BearerAuth",
        responses={
            200: ("Document was removed", message_model),
            401: ("Missing JWT in headers or cookie", message_model),
            404: ("User does not have such collection or document",
                  message_model),
            409: ("Document is not part of this collection", message_model),
        }
    )
    @ensure_user_collection_exists
    @ensure_user_document_exists
    @ensure_document_in_collection
    def delete(self, collection_id, document_id):
        """Remove document from collection"""
        delete_document_from_collection(collection_id, document_id)
        return {"message": "Document was deleted from this collection"}, 200
