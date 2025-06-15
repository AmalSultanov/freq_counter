from datetime import datetime

from app.database import db


class DocumentModel(db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    contents = db.Column(db.Text, nullable=False)
    content_hash = db.Column(db.String(64), index=True, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    collections = db.relationship(
        "DocumentCollectionModel",
        cascade="all, delete-orphan",
        back_populates="document"
    )

    def __repr__(self):
        return f"<DocumentModel {self.id}: {self.name}>"

    def __str__(self):
        return self.name
