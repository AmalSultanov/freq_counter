from app.users.models import UserModel
from app.database import db
from app.collections.models import CollectionModel
from app.documents.services.checks import is_user_document_present
from app.shared.common_models import DocumentCollectionModel


def user_collection_exists(user: UserModel, collection_id: int) -> bool:
    return (
        db.session.query(CollectionModel)
        .filter_by(id=collection_id, user_id=user.id)
        .first()
    ) is not None


def user_collection_with_name_exists(
    user: UserModel, collection_name: str
) -> bool:
    return (
        db.session.query(CollectionModel)
        .filter_by(name=collection_name, user_id=user.id)
        .first()
    ) is not None


def user_document_exists(user: UserModel, document_id: int) -> bool:
    return is_user_document_present(document_id, user)


def document_in_collection_exists(
    collection_id: int, document_id: int
) -> bool:
    return (
        db.session.query(DocumentCollectionModel)
        .filter_by(collection_id=collection_id, document_id=document_id)
        .first()
    ) is not None

