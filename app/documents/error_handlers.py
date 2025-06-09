from flask import jsonify

from app.shared.exceptions import DuplicateDocumentError, EmptyFileError


def register_documents_errors_handlers(bp):
    @bp.errorhandler(DuplicateDocumentError)
    def handle_duplicate_document(error):
        return jsonify({"message": str(error)}), 409

    @bp.errorhandler(EmptyFileError)
    def handle_empty_document(error):
        return jsonify({"message": str(error)}), 400
