import os

from werkzeug.datastructures import FileStorage

from app.extensions import cache
from app.database import db
from app.documents.models import DocumentModel
from app.documents.selectors import get_user_document
from app.documents.services.checks import check_for_duplicates
from app.shared.file_utils import save_uploaded_file, compute_content_hash
from app.system.services import create_document_metrics
from app.users.services import get_user_by_username


def handle_document_upload(file: FileStorage, username: str) -> DocumentModel:
    file_path, contents = save_uploaded_file(file, username)
    user = get_user_by_username(username)
    content_hash = compute_content_hash(contents.lower())

    check_for_duplicates(user.id, content_hash)

    document = create_and_store_document(
        file_path, contents, content_hash, user.id
    )

    record_document_metrics(document.id, file_path, contents)

    return document


def create_and_store_document(
    file_path: str, contents: str, content_hash: str, user_id: int
) -> DocumentModel:
    document = create_document(
        os.path.basename(file_path), contents, content_hash, user_id
    )

    db.session.add(document)
    db.session.commit()

    return document


def record_document_metrics(
    document_id: int, file_path: str, contents: str
) -> None:
    create_document_metrics(
        document_id,
        len(contents.split()),
        os.path.getsize(file_path)
    )


def create_document(name, contents, content_hash, user_id) -> DocumentModel:
    return DocumentModel(
        name=name, contents=contents,
        content_hash=content_hash, user_id=user_id
    )


def remove_document(username: str, document_id: int) -> DocumentModel | None:
    document = get_user_document(username, document_id)

    if not document:
        return None

    db.session.delete(document)
    db.session.commit()
    cache.delete(f"tf:{document_id}")

    return document
