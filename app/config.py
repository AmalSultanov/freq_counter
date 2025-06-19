import os
from datetime import timedelta

from dotenv import load_dotenv

load_dotenv()


def str_to_bool(value: str) -> bool:
    return str(value).strip().lower() in ("true", "1")


flask_port = os.getenv("FLASK_PORT")
flask_debug = str_to_bool(os.getenv("FLASK_DEBUG"))
flask_env = os.getenv("FLASK_ENV")
flask_secret_key = os.getenv("FLASK_SECRET_KEY")
flask_admin_secret_key = os.getenv("FLASK_ADMIN_SECRET_KEY")

jwt_secret_key = os.getenv("JWT_SECRET_KEY")
jwt_cookie_csrf_protect = str_to_bool(os.getenv("JWT_COOKIE_CSRF_PROTECT"))
jwt_cookie_secure = str_to_bool(os.getenv("JWT_COOKIE_SECURE"))
jwt_access_token_expires_minutes = int(os.getenv(
    "JWT_ACCESS_TOKEN_EXPIRES_MINUTES"
))
jwt_refresh_token_expires_days = int(os.getenv(
    "JWT_REFRESH_TOKEN_EXPIRES_DAYS"
))

redis_host = os.getenv("CACHE_REDIS_HOST")
redis_port = os.getenv("CACHE_REDIS_PORT")

postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_host = os.getenv("POSTGRES_HOST")
postgres_port = os.getenv("POSTGRES_PORT")
postgres_db = os.getenv("POSTGRES_DB")


class Config:
    DEBUG = flask_debug
    SECRET_KEY = flask_secret_key
    ADMIN_SECRET_KEY = flask_admin_secret_key
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{postgres_user}:{postgres_password}"
        f"@{postgres_host}:{postgres_port}/{postgres_db}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MEDIA_FOLDER = os.path.join(os.path.dirname(__file__), "media")
    JWT_SECRET_KEY = jwt_secret_key
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
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
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = redis_host
    CACHE_REDIS_PORT = redis_port
    CACHE_KEY_PREFIX = ""


class DevelopmentConfig(Config):
    pass


class ProductionConfig(Config):
    pass


config_by_name = {"dev": DevelopmentConfig, "prod": ProductionConfig}
