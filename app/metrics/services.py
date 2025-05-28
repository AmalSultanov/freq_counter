from datetime import date

from sqlalchemy import func

from app import db
from app.metrics.models import FileMetricModel


def create_file_metric(
    filename: str, word_count: int, file_size: int
) -> FileMetricModel:
    metric = FileMetricModel(
        filename=filename, word_count=word_count, file_size=file_size
    )

    db.session.add(metric)
    db.session.commit()

    return metric


def get_uploads_count() -> int | None:
    today = date.today()
    result = (
        db.session.query(func.count().label("uploads_count"))
        .filter(func.date(FileMetricModel.created_at) == today)
        .scalar()
    )

    return result


def get_largest_file() -> int | None:
    largest_size = (
        db.session.query(FileMetricModel.file_size)
        .order_by(FileMetricModel.file_size.desc())
        .limit(1)
        .scalar()
    )
    return largest_size
