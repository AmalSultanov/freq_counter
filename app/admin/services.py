from app.database import db
from app.config import flask_admin_secret_key
from app.users.models import UserModel
from app.users.services import get_user_by_username, create_user


def is_admin_secret_key_valid(admin_secret_key: str) -> bool:
    return admin_secret_key == flask_admin_secret_key


def register_admin(username: str, password: str) -> None | UserModel:
    user = get_user_by_username(username)

    if user:
        if user.is_admin:
            return None

        user.is_admin = True
        db.session.commit()

        return user
    return create_admin(username, password)


def create_admin(username: str, password: str) -> UserModel:
    user = create_user(username, password)
    user.is_admin = True
    db.session.commit()

    return user
