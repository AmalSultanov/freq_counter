from flask_restx import fields

from app.documents.namespace import api

document_model = api.model("Document", {
    "document_id": fields.Integer,
    "document_name": fields.String
})

document_content_model = api.model("DocumentContent", {
    "document_id": fields.Integer,
    "document_contents": fields.String
})

huffman_encoded_document_content_model = api.model(
    "HuffmanEncodedDocumentContent",
    {
        "document_id": fields.Integer,
        "huffman_encoded_document_contents": fields.String
    }
)

statistics_model = api.model("DocumentStatistics", {
    "document_id": fields.Integer(required=True),
    "tf": fields.Raw(required=False),
    "collections_data": fields.Raw(required=False),
    "message": fields.String(required=False)
})

message_model = api.model("Message", {
    "message": fields.String
})
