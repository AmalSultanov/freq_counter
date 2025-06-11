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

statistics_model = api.model("DocumentStatistics", {
    "document_id": fields.Integer(required=True, description="ID of the document"),
    "tf": fields.Raw(required=False, description="Term Frequency for this document (if IDF is unavailable)"),
    "collections_data": fields.Raw(required=False, description="TF and IDF statistics for each collection"),
    "message": fields.String(required=False, description="Displayed if the document is not part of any collection")
})

message_model = api.model("Message", {
    "message": fields.String
})
