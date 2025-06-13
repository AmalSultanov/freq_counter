from collections import Counter

from sqlalchemy import Row

from app.collections.models import CollectionModel
from app.database import db
from app.documents.models import DocumentModel
from app.documents.services import (
    get_documents_in_collection, get_document_by_id, is_user_document_present
)
from app.shared.common_models import DocumentCollectionModel
from app.shared.tfidf_stats import (
    tokenize_text, calculate_tf, calculate_idf, get_least_frequent_words
)
from app.users.models import UserModel
from app.users.services import get_user_by_username


def add_collection(username: str, collection_name: str) -> CollectionModel:
    user = get_user_by_username(username)
    collection = CollectionModel(name=collection_name, user_id=user.id)

    db.session.add(collection)
    db.session.commit()

    return collection


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

    all_text = get_collection_documents_text(collection_id)
    tokens = tokenize_text(all_text)
    total_words = len(tokens)
    word_counts = Counter(tokens)

    tf_dict = calculate_tf(word_counts, total_words)
    least_frequent_words = get_least_frequent_words(tf_dict)
    tf = {word: tf_dict[word] for word in least_frequent_words}

    if number_of_documents == 1:
        return 1, tf, {}

    idf_dict = calculate_idf(documents_in_collection)
    idf = {word: idf_dict.get(word, 0.0) for word in least_frequent_words}

    return number_of_documents, tf, idf


def get_collection_documents_text(collection_id: int) -> str:
    documents = (
        db.session.query(DocumentModel.contents)
        .join(DocumentCollectionModel,
              DocumentModel.id == DocumentCollectionModel.document_id)
        .filter(DocumentCollectionModel.collection_id == collection_id)
        .all()
    )

    return " ".join(document.contents for document in documents)


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

    return link


def delete_document_from_collection(
    collection_id: int, document_id: int
) -> DocumentCollectionModel | None:
    link = (
        db.session.query(DocumentCollectionModel)
        .filter_by(collection_id=collection_id, document_id=document_id)
        .first()
    )

    if link:
        db.session.delete(link)
        db.session.commit()

        return link
    return None


def update_collection_name(
    username: str, collection_id: int, collection_name: str
) -> None | CollectionModel:
    user_collection = get_user_collection(username, collection_id)

    if not user_collection:
        return None

    user_collection.name = collection_name
    db.session.commit()

    return user_collection


def remove_collection(
        username: str, collection_id: int
) -> CollectionModel | None:
    user = get_user_by_username(username)
    collection = (
        db.session.query(CollectionModel)
        .filter_by(id=collection_id, user_id=user.id)
        .first()
    )

    if not collection:
        return None

    db.session.delete(collection)
    db.session.commit()

    return collection
