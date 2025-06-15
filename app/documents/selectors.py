from sqlalchemy import Row

from app.extensions import cache
from app.database import db
from app.documents.models import DocumentModel
from app.shared.common_models import DocumentCollectionModel
from app.shared.tfidf_stats import get_document_tf
from app.users.services import get_user_by_username


def get_documents_by_username(username: str) -> list[Row]:
    user = get_user_by_username(username)

    return (
        db.session.query(DocumentModel.id, DocumentModel.name)
        .filter(DocumentModel.user_id == user.id)
        .all()
    )


def get_user_document(username: str, document_id: int):
    user = get_user_by_username(username)

    return (
        db.session.query(DocumentModel)
        .filter(
            DocumentModel.id == document_id, DocumentModel.user_id == user.id
        )
        .first()
    )


def get_document_by_id(document_id: int) -> DocumentModel | None:
    return db.session.query(DocumentModel).filter_by(id=document_id).first()


def fetch_document_contents(document_id: int) -> str | None:
    document = (
        db.session.query(DocumentModel.contents)
        .filter(DocumentModel.id == document_id)
        .scalar()
    )

    return document if document else None


def get_document_tf_cached(document_id: int) -> dict[str, float] | None:
    cache_key = f"tf:{document_id}"
    cached_tf = cache.get(cache_key)

    if cached_tf is not None:
        return cached_tf

    document_contents = fetch_document_contents(document_id)
    tf = get_document_tf(document_contents)
    cache.set(cache_key, tf, timeout=6 * 3600)

    return tf


def get_collections_idf_data(
    document_id: int, tf: dict[str, float]
) -> list[dict[str, int | dict[str, float] | str]] | None:
    collections = get_collections_for_document(document_id)

    if not collections:
        return None

    return [
        get_collection_idf_data(collection_id, tf)
        for collection_id in collections
    ]


def get_collection_idf_data(
    collection_id: int, tf: dict[str, float]
) -> dict[str, int | dict[str, float] | str]:
    documents = get_documents_in_collection(collection_id)
    number_of_documents = len(documents)

    if number_of_documents == 1:
        return {
            "collection_id": collection_id,
            "tf": tf,
            "message": (
                "This document is the only one in this "
                "collection, IDF is unavailable"
            )
        }

    from app.collections.selectors import get_collection_idf_cached
    idf = get_collection_idf_cached(collection_id, list(tf.keys()))

    return {
        "collection_id": collection_id,
        "tf": tf,
        "idf": idf
    }


def get_collections_for_document(document_id: int) -> list[int]:
    collection_ids = (
        db.session.query(DocumentCollectionModel.collection_id)
        .filter(DocumentCollectionModel.document_id == document_id)
        .all()
    )

    return [collection_id.collection_id for collection_id in collection_ids]


def get_documents_in_collection(collection_id: int) -> list[tuple[int, str]]:
    documents = (
        db.session.query(DocumentModel.id, DocumentModel.contents)
        .join(DocumentCollectionModel,
              DocumentModel.id == DocumentCollectionModel.document_id)
        .filter(DocumentCollectionModel.collection_id == collection_id)
        .all()
    )

    return documents
