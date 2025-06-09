import hashlib
import os

from flask import current_app
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from app.shared.exceptions import EmptyFileError


def compute_content_hash(content: str) -> str:
    return hashlib.sha256(content.encode('utf-8')).hexdigest()


def is_file_invalid(file: FileStorage) -> bool:
    return not file or not file.filename.endswith(".txt")


def save_uploaded_file(file: FileStorage, username: str) -> tuple[str, str]:
    filename, contents = extract_file_contents(file)
    user_folder = get_user_media_path(username)
    file_path = os.path.join(user_folder, filename)
    write_file_to_disk(file_path, contents)

    return file_path, contents


def extract_file_contents(file: FileStorage) -> tuple[str, str]:
    filename = secure_filename(file.filename)
    contents = file.read().decode("utf-8")

    if not contents:
        raise EmptyFileError("Uploading empty files is not allowed")

    return filename, contents


def get_user_media_path(username: str) -> str:
    media_path = current_app.config["MEDIA_FOLDER"]
    user_media_path = os.path.join(media_path, username)
    os.makedirs(user_media_path, exist_ok=True)

    return user_media_path


def write_file_to_disk(file_path: str, contents: str) -> None:
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(contents)
