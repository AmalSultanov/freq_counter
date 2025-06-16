import os
from collections import Counter

import pandas as pd
from flask import current_app
from pandas import DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename


def get_table_data(file: FileStorage) -> list[dict[str, str | float | int]]:
    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config["MEDIA_FOLDER"], filename)
    file.save(filepath)

    content = read_file(filepath)
    df = create_df_from_text(content)

    return df.to_dict(orient="records")


def read_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def create_df_from_text(text: str) -> DataFrame:
    tokens = tokenize_text(text)
    total_words = len(tokens)
    word_counts = Counter(tokens)
    table_data = calculate_tf_idf(word_counts, total_words)

    return get_sorted_df(table_data)


def tokenize_text(text: str) -> list[str]:
    vectorizer = TfidfVectorizer(use_idf=False, norm=None)
    analyzer = vectorizer.build_analyzer()

    return analyzer(text)


def calculate_tf_idf(
    word_counts: Counter, total_words: int
) -> dict[str, list[str | float | int]]:
    table_data = {"word": [], "tf": [], "idf": []}

    for word, count in word_counts.items():
        table_data["word"].append(word)
        table_data["tf"].append(round(count / total_words, 3))
        # log10(1/1) = 0 for all words since only 1 document is uploaded
        table_data["idf"].append(0)

    return table_data


def get_sorted_df(table_data: dict[str, list[str | float | int]]) -> DataFrame:
    df = pd.DataFrame(table_data)
    return df.sort_values(by="idf", ascending=False).head(50)
