from flask import jsonify
from flask_jwt_extended.exceptions import CSRFError


def register_error_handlers(app):
    @app.errorhandler(CSRFError)
    def handle_csrf_error(e):
        return jsonify({"message": str(e)}), 401
