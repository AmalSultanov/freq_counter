from flask_restx import fields

from app.collections.namespace import api

collection_input = api.model("CollectionInput", {
    "collection_name": fields.String(required=True)
})

document_response = api.model("Document", {
    "document_id": fields.Integer,
    "document_name": fields.String
})

collection_response = api.model("Collection", {
    "collection_id": fields.Integer,
    "documents": fields.List(fields.Nested(document_response))
})

statistics_response = api.model("CollectionStatistics", {
    "collection_id": fields.Integer,
    "tf": fields.Raw,
    "idf": fields.Raw,
    "message": fields.String
})

message_model = api.model("Message", {
    "message": fields.String
})
