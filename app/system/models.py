from datetime import datetime

from app.database import db


class FileMetricModel(db.Model):
    __tablename__ = "file_metrics"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(256), nullable=False)
    word_count = db.Column(db.Integer, nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<FileMetricModel {self.id}: {self.filename}>"

    def __str__(self):
        return self.filename
