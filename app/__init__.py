import os

from flask import Flask
from flask_migrate import Migrate

from app.config import config_by_name, flask_env
from app.database import db
from app.metrics.routes import metrics_bp
from app.tfidf.routes import tfidf_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_by_name.get(flask_env))

    os.makedirs(app.config["MEDIA_FOLDER"], exist_ok=True)
    db.init_app(app)
    Migrate(app, db)

    from app.metrics.models import FileMetricModel

    app.register_blueprint(tfidf_bp)
    app.register_blueprint(metrics_bp)

    return app
