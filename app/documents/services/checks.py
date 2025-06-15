from app.database import db
from app.documents.models import DocumentModel
from app.users.models import UserModel
from app.shared.exceptions import DuplicateDocumentError


def check_for_duplicates(user_id: int, content_hash: str) -> None:
    if is_duplicate_document(user_id, content_hash):
        message = "Document with this content was already uploaded earlier"
        raise DuplicateDocumentError(message)


def is_duplicate_document(user_id: int, content_hash: str) -> bool:
    existing_document = (
        db.session.query(DocumentModel)
        .filter_by(user_id=user_id, content_hash=content_hash)
        .first()
    )
    return existing_document is not None


def is_user_document_present(document_id: int, user: UserModel) -> bool:
    return (
        db.session.query(DocumentModel)
        .filter_by(id=document_id, user_id=user.id)
        .first()
    ) is not None


def user_has_document(user: UserModel, document_id: int) -> bool:
    return (
        db.session.query(DocumentModel)
        .filter(
            DocumentModel.id == document_id, DocumentModel.user_id == user.id
        )
        .first()
    ) is not None
