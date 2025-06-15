from datetime import datetime

from app.database import db


class CollectionModel(db.Model):
    __tablename__ = "collections"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    documents = db.relationship(
        "DocumentCollectionModel",
        cascade="all, delete-orphan",
        back_populates="collection"
    )

    def __repr__(self):
        return f"<CollectionModel {self.id}: {self.name}>"

    def __str__(self):
        return self.name
