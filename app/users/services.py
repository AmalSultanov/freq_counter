from flask_jwt_extended import create_access_token, create_refresh_token

from app.database import db
from app.users.models import UserModel


def register_user(username: str, password: str) -> None | UserModel:
    if db.session.query(UserModel).filter_by(username=username).first():
        return None

    user = UserModel(username=username)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user


def authenticate_user(username: str, password: str) -> dict[str, str]:
    user = db.session.query(UserModel).filter_by(username=username).first()

    if user is None:
        return {"message": "User with this username does not exist"}

    if not user.check_password(password):
        return {"message": "Invalid password"}

    return generate_tokens(user.username)


def generate_tokens(username: str) -> dict[str, str]:
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)

    return {"access_token": access_token, "refresh_token": refresh_token}


def change_user_password(user_id: int, new_password: str) -> None | UserModel:
    user = get_user_by_id(user_id)

    if user.check_password(new_password):
        return None

    user.set_password(new_password)
    db.session.commit()

    return user


def get_user_by_id(user_id: int) -> UserModel | None:
    user = db.session.query(UserModel).filter_by(id=user_id).scalar()
    return user if user is not None else None


def get_user_by_username(username: str) -> UserModel | None:
    user = db.session.query(UserModel).filter_by(username=username).scalar()
    return user if user is not None else None


def remove_user(user_id: int) -> None | UserModel:
    user = db.session.query(UserModel).filter_by(id=user_id).first()

    if not user:
        return None

    db.session.delete(user)
    db.session.commit()

    return user
