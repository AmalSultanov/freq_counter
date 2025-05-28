import os

from dotenv import load_dotenv

load_dotenv()

flask_port = os.getenv("FLASK_PORT")
flask_debug = os.getenv("FLASK_DEBUG")
flask_env = os.getenv("FLASK_ENV")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_host = os.getenv("POSTGRES_HOST")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_db = os.getenv("POSTGRES_DB")


class Config:
    DEBUG = flask_debug
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{postgres_user}:{postgres_password}"
        f"@{postgres_host}:{postgres_port}/{postgres_db}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MEDIA_FOLDER = os.path.join(os.path.dirname(__file__), "media")


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config_by_name = {"dev": DevelopmentConfig, "prod": ProductionConfig}
