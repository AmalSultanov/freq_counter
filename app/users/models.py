from datetime import datetime

from flask_bcrypt import generate_password_hash, check_password_hash

from app.database import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    documents = db.relationship(
        "DocumentModel",
        backref="user",
        cascade="all, delete-orphan"
    )
    collections = db.relationship(
        "CollectionModel",
        backref="user",
        cascade="all, delete-orphan"
    )

    def set_password(self, password: str):
        self.password = generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<UserModel {self.id}: {self.username}>"

    def __str__(self):
        return self.username
