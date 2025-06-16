from datetime import datetime

from app.database import db


class DocumentMetricModel(db.Model):
    __tablename__ = "document_metrics"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    document_id = db.Column(
        db.Integer,
        db.ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )
    word_count = db.Column(db.Integer, nullable=False)
    size = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    document = db.relationship(
        "DocumentModel", back_populates="document_metric"
    )

    def __repr__(self):
        return (f"<DocumentMetricModel {self.id}: "
                f"word_count={self.word_count}, size={self.size}>")
