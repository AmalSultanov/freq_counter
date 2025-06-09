import os

from flask import Flask, Blueprint, redirect
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_swagger_ui import get_swaggerui_blueprint

from app.collections.api_routes import collections_api_bp
from app.config import config_by_name, flask_env
from app.database import db
from app.documents.api_routes import documents_api_bp
from app.system.api_routes import system_api_bp
from app.tfidf.routes import tfidf_bp
from app.users.api_routes import users_api_bp

bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_by_name.get(flask_env))

    os.makedirs(app.config["MEDIA_FOLDER"], exist_ok=True)
    db.init_app(app)
    Migrate(app, db)

    bcrypt.init_app(app)
    jwt.init_app(app)

    from app.system.models import FileMetricModel
    from app.collections.models import CollectionModel
    from app.documents.models import DocumentModel
    from app.users.models import UserModel
    from app.shared.common_models import DocumentCollectionModel

    @app.route("/")
    def index():
        return redirect("/tfidf")

    api_bp = Blueprint("api", __name__, url_prefix="/api")
    api_bp.register_blueprint(system_api_bp, url_prefix="/system")
    api_bp.register_blueprint(documents_api_bp, url_prefix="/documents")
    api_bp.register_blueprint(collections_api_bp, url_prefix="/collections")
    api_bp.register_blueprint(users_api_bp, url_prefix="/users")

    swaggerui_bp = get_swaggerui_blueprint("/api/docs", "/static/swagger.json")

    app.register_blueprint(swaggerui_bp, url_prefix="/api/docs")
    app.register_blueprint(api_bp)
    app.register_blueprint(tfidf_bp, url_prefix="/tfidf")

    return app
