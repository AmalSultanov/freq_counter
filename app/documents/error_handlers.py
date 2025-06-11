from flask_jwt_extended.exceptions import (
    NoAuthorizationError, InvalidHeaderError
)

from app.shared.exceptions import DuplicateDocumentError, EmptyFileError


def register_documents_errors_handlers(api):
    @api.errorhandler(NoAuthorizationError)
    @api.errorhandler(InvalidHeaderError)
    def handle_auth_error(error):
        return {"message": str(error)}, 401

    @api.errorhandler(DuplicateDocumentError)
    def handle_duplicate_document(error):
        return {"message": str(error)}, 409

    @api.errorhandler(EmptyFileError)
    def handle_empty_document(error):
        return {"message": str(error)}, 400
