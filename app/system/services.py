from datetime import date

from sqlalchemy import func

from app.database import db
from app.system.models import DocumentMetricModel


def create_document_metrics(
    document_id: int, word_count: int, size: int
) -> DocumentMetricModel:
    metric = DocumentMetricModel(
        document_id=document_id, word_count=word_count, size=size
    )

    db.session.add(metric)
    db.session.commit()

    return metric


def get_uploads_count() -> int:
    today = date.today()
    result = (
        db.session.query(func.count().label("uploads_count"))
        .filter(func.date(DocumentMetricModel.created_at) == today)
        .scalar()
    )

    return result or 0


def get_largest_file() -> int:
    largest_size = (
        db.session.query(DocumentMetricModel.size)
        .order_by(DocumentMetricModel.size.desc())
        .limit(1)
        .scalar()
    )

    return largest_size or 0
