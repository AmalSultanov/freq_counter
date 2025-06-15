from sqlalchemy import Row

from app.extensions import cache
from app.collections.models import CollectionModel
from app.database import db
from app.documents.models import DocumentModel
from app.documents.selectors import (
    get_documents_in_collection, get_document_tf_cached
)
from app.shared.common_models import DocumentCollectionModel
from app.shared.tfidf_stats import calculate_idf, get_document_tf

from app.users.models import UserModel
from app.users.services import get_user_by_username


def get_collection_by_id(collection_id: int) -> CollectionModel | None:
    return (
        db.session.query(CollectionModel)
        .filter_by(id=collection_id)
        .first()
    )


def get_user_collection(username: str, collection_id: int) -> UserModel | None:
    user = get_user_by_username(username)
    return (
        db.session.query(CollectionModel)
        .filter_by(id=collection_id, user_id=user.id)
        .first()
    )


def get_collections_list(username: str) -> list[CollectionModel]:
    user = get_user_by_username(username)
    return (
        db.session.query(CollectionModel)
        .filter(CollectionModel.user_id == user.id)
        .all()
    )


def get_documents_by_collection_id(collection_id: int) -> list[Row]:
    return (
        db.session.query(DocumentCollectionModel.document_id)
        .filter(DocumentCollectionModel.collection_id == collection_id)
        .all()
    )


def get_collection_stats(
    collection_id: int
) -> tuple[int, dict[str, float], dict[str, float]]:
    documents_in_collection = get_documents_in_collection(collection_id)
    number_of_documents = len(documents_in_collection)

    if number_of_documents == 0:
        return 0, {}, {}

    if number_of_documents == 1:
        document_id = documents_in_collection[0][0]
        tf = get_document_tf_cached(document_id)

        return 1, tf, {}

    tf = get_collection_tf_cached(collection_id)
    idf = get_collection_idf_cached(collection_id, list(tf.keys()))

    return number_of_documents, tf, idf


def get_collection_tf_cached(collection_id: int) -> dict[str, float]:
    cache_key = f"collection_tf:{collection_id}"
    cached_tf = cache.get(cache_key)

    if cached_tf is not None:
        return cached_tf

    all_text = get_collection_documents_text(collection_id)
    tf = get_document_tf(all_text)
    cache.set(cache_key, tf, timeout=6 * 3600)

    return tf


def get_collection_idf_cached(
    collection_id: int, words: list[str]
) -> dict[str, float]:
    cache_key = f"collection_idf:{collection_id}"
    cached_idf = cache.get(cache_key)

    if cached_idf is not None:
        return {word: cached_idf.get(word, 0.0) for word in words}

    documents_in_collection = get_documents_in_collection(collection_id)
    idf_dict = calculate_idf(documents_in_collection)
    print(idf_dict)
    print({word: idf_dict.get(word, 0.0) for word in words})
    cache.set(cache_key, idf_dict, timeout=6 * 3600)

    return {word: idf_dict.get(word, 0.0) for word in words}


def get_collection_documents_text(collection_id: int) -> str:
    documents = (
        db.session.query(DocumentModel.contents)
        .join(DocumentCollectionModel,
              DocumentModel.id == DocumentCollectionModel.document_id)
        .filter(DocumentCollectionModel.collection_id == collection_id)
        .all()
    )

    return " ".join(document.contents for document in documents)
