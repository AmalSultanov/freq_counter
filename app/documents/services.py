import os
from collections import Counter

from sqlalchemy import Row
from werkzeug.datastructures import FileStorage

from app.database import db
from app.documents.models import DocumentModel
from app.shared.common_models import DocumentCollectionModel
from app.shared.exceptions import DuplicateDocumentError
from app.shared.file_utils import save_uploaded_file, compute_content_hash
from app.shared.tfidf_stats import (
    tokenize_text, calculate_tf, get_least_frequent_words, calculate_idf
)
from app.system.services import create_file_metric
from app.users.models import UserModel
from app.users.services import get_user_by_username


def add_document(file: FileStorage, username: str) -> DocumentModel:
    file_path, contents = save_uploaded_file(file, username)
    user = get_user_by_username(username)
    content_hash = compute_content_hash(contents)

    if is_duplicate_document(user.id, content_hash):
        message = "Document with this content was already uploaded earlier"
        raise DuplicateDocumentError(message)

    document = create_document(
        os.path.basename(file_path), contents, content_hash, user.id
    )

    create_file_metric(
        os.path.basename(file_path),
        len(contents.split()),
        os.path.getsize(file_path)
    )

    db.session.add(document)
    db.session.commit()

    return document


def create_document(name, contents, content_hash, user_id) -> DocumentModel:
    return DocumentModel(
        name=name, contents=contents,
        content_hash=content_hash, user_id=user_id
    )


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


def get_documents_by_username(username: str) -> list[Row]:
    user = get_user_by_username(username)

    return (
        db.session.query(DocumentModel.id, DocumentModel.name)
        .filter(DocumentModel.user_id == user.id)
        .all()
    )


def get_document_by_id(document_id: int) -> DocumentModel | None:
    return db.session.query(DocumentModel).filter_by(id=document_id).first()


def fetch_document_contents(document_id: int) -> Row | None:
    document = (
        db.session.query(DocumentModel.id, DocumentModel.contents)
        .filter(DocumentModel.id == document_id)
        .first()
    )

    return document if document else None


def get_collections_idf_data(
    document_id: int, tf: dict[str, float]
) -> list[dict[str, int | dict[str, float]]] | None:
    collections = get_collections_for_document(document_id)

    if not collections:
        return None

    collections_data = []

    for collection_id in collections:
        documents_in_collection = get_documents_in_collection(collection_id)
        idf = calculate_idf(documents_in_collection)
        tfidf = {
            "collection_id": collection_id,
            "tf": tf,
            "idf": {word: idf.get(word, 0.0) for word in tf}
        }
        collections_data.append(tfidf)

    return collections_data


def get_collections_for_document(document_id: int) -> list[int]:
    collection_ids = (
        db.session.query(DocumentCollectionModel.collection_id)
        .filter(DocumentCollectionModel.document_id == document_id)
        .all()
    )

    return [collection_id.collection_id for collection_id in collection_ids]


def get_document_tf(document_id: int) -> dict[str, float] | None:
    document_contents = (
        db.session.query(DocumentModel.contents)
        .filter_by(id=document_id)
        .scalar()
    )

    if document_contents:
        tokens = tokenize_text(document_contents)
        total_words = len(tokens)
        word_counts = Counter(tokens)
        tf_dict = calculate_tf(word_counts, total_words)
        least_frequent_words = get_least_frequent_words(tf_dict)
        tf = {word: tf_dict[word] for word in least_frequent_words}

        return tf
    return None


def get_documents_in_collection(collection_id: int) -> list[tuple[int, str]]:
    documents = (
        db.session.query(DocumentModel.id, DocumentModel.contents)
        .join(DocumentCollectionModel,
              DocumentModel.id == DocumentCollectionModel.document_id)
        .filter(DocumentCollectionModel.collection_id == collection_id)
        .all()
    )

    return documents


def remove_document(document_id: int, username: str) -> DocumentModel | None:
    user = get_user_by_username(username)
    document = (
        db.session.query(DocumentModel)
        .filter(
            DocumentModel.id == document_id, DocumentModel.user_id == user.id
        )
        .first()
    )

    if not document:
        return None

    db.session.delete(document)
    db.session.commit()

    return document


def user_has_document(document_id: int, user: UserModel) -> bool:
    return (
        db.session.query(DocumentModel)
        .filter(
            DocumentModel.id == document_id, DocumentModel.user_id == user.id
        )
        .first()
    ) is not None
