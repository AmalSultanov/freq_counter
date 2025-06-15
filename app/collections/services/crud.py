from app.extensions import cache
from app.collections.models import CollectionModel
from app.collections.selectors import get_collection_by_id, get_user_collection
from app.database import db
from app.documents.selectors import get_document_by_id
from app.shared.common_models import DocumentCollectionModel
from app.users.services import get_user_by_username


def add_collection(username: str, collection_name: str) -> CollectionModel:
    user = get_user_by_username(username)
    collection = CollectionModel(name=collection_name, user_id=user.id)

    db.session.add(collection)
    db.session.commit()

    return collection


def add_document_to_collection(
    collection_id: int, document_id: int
) -> DocumentCollectionModel | None:
    collection = get_collection_by_id(collection_id)
    document = get_document_by_id(document_id)

    if not collection or not document:
        return None

    link = DocumentCollectionModel(
        collection_id=collection_id, document_id=document_id
    )
    db.session.add(link)
    db.session.commit()
    cache.delete(f"collection_tf:{collection_id}")
    cache.delete(f"collection_idf:{collection_id}")

    return link


def update_collection_name(
    username: str, collection_id: int, collection_name: str
) -> None | CollectionModel:
    user_collection = get_user_collection(username, collection_id)
    user_collection.name = collection_name
    db.session.commit()

    return user_collection


def delete_document_from_collection(
    collection_id: int, document_id: int
) -> DocumentCollectionModel | None:
    link = (
        db.session.query(DocumentCollectionModel)
        .filter_by(collection_id=collection_id, document_id=document_id)
        .first()
    )

    if not link:
        return None

    db.session.delete(link)
    db.session.commit()
    cache.delete(f"collection_tf:{collection_id}")
    cache.delete(f"collection_idf:{collection_id}")

    return link


def remove_collection(
    username: str, collection_id: int
) -> CollectionModel | None:
    collection = get_user_collection(username, collection_id)
    db.session.delete(collection)
    db.session.commit()
    cache.delete(f"collection_tf:{collection_id}")
    cache.delete(f"collection_idf:{collection_id}")

    return collection
