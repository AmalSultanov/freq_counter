import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()

flask_port = os.getenv("FLASK_PORT")
flask_debug = os.getenv("FLASK_DEBUG")
flask_env = os.getenv("FLASK_ENV")

jwt_secret_key = os.getenv("JWT_SECRET_KEY")
jwt_cookie_csrf_protect = os.getenv("JWT_COOKIE_CSRF_PROTECT")
jwt_cookie_secure = os.getenv("JWT_COOKIE_SECURE")
jwt_access_token_expires_minutes = int(os.getenv(
    "JWT_ACCESS_TOKEN_EXPIRES_MINUTES"
))
jwt_refresh_token_expires_days = int(os.getenv(
    "JWT_REFRESH_TOKEN_EXPIRES_DAYS"
))

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
    JWT_SECRET_KEY = jwt_secret_key
    JWT_TOKEN_LOCATION = "cookies"
    JWT_ACCESS_COOKIE_PATH = "/"
    JWT_REFRESH_COOKIE_PATH = "/api/users/refresh"
    JWT_COOKIE_CSRF_PROTECT = jwt_cookie_csrf_protect
    JWT_COOKIE_SECURE = jwt_cookie_secure
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(
        minutes=jwt_access_token_expires_minutes
    )
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(
        days=jwt_refresh_token_expires_days
    )


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config_by_name = {"dev": DevelopmentConfig, "prod": ProductionConfig}
