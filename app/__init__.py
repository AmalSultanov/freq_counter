import os

from flask import Flask, redirect
from flask_migrate import Migrate
from flask_restx import Api

from app.admin import admin, views
from app.admin.routes import admin_bp
from app.collections import api_routes
from app.collections.namespace import api as collections_ns
from app.config import config_by_name, flask_env
from app.database import db
from app.documents import api_routes
from app.documents.namespace import api as documents_ns
from app.extensions import bcrypt, jwt, cache
from app.shared.error_handlers import register_error_handlers
from app.system import api_routes
from app.system.namespace import api as system_ns
from app.tfidf.routes import tfidf_bp
from app.users import api_routes
from app.users.namespace import api as users_ns
from app.version import __version__

authorizations = {
    'BearerAuth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "JWT Authorization header using the Bearer scheme. "
                       "Example: 'Bearer {token}'"
    }
}


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_by_name.get(flask_env))

    os.makedirs(app.config["MEDIA_FOLDER"], exist_ok=True)
    db.init_app(app)
    Migrate(app, db)

    admin.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    cache.init_app(app)

    register_error_handlers(app)

    from app.system.models import DocumentMetricModel
    from app.collections.models import CollectionModel
    from app.documents.models import DocumentModel
    from app.users.models import UserModel
    from app.shared.common_models import DocumentCollectionModel

    @app.route("/")
    def index():
        return redirect("/tfidf")

    api = Api(
        app,
        version=__version__,
        title="Word Frequency Counter: TF-IDF Analyzer API",
        description="API for TF-IDF calculations on documents and collections "
                    "managed by users. Also includes system-level endpoints.",
        authorizations=authorizations,
        doc="/api/docs"
    )

    api.add_namespace(users_ns, path="/api/users")
    api.add_namespace(documents_ns, path="/api/documents")
    api.add_namespace(collections_ns, path="/api/collections")
    api.add_namespace(system_ns, path="/api/system")

    app.register_blueprint(tfidf_bp, url_prefix="/tfidf")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    return app
