from datetime import datetime

from app.database import db


class DocumentCollectionModel(db.Model):
    __tablename__ = "documents_collections"

    document_id = db.Column(
        db.Integer,
        db.ForeignKey("documents.id"),
        primary_key=True,
        nullable=False
    )
    collection_id = db.Column(
        db.Integer,
        db.ForeignKey("collections.id"),
        primary_key=True,
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    document = db.relationship("DocumentModel", back_populates="collections")
    collection = db.relationship("CollectionModel", back_populates="documents")

    def __repr__(self):
        keys = f"{self.document_id}, {self.collection_id}"
        return f"<DocumentCollectionModel: ({keys})>"
