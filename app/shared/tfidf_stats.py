from collections import Counter

import math
from sklearn.feature_extraction.text import TfidfVectorizer


def get_word_stats(text: str) -> tuple[Counter[str], int]:
    tokens = tokenize_text(text)
    total_words = len(tokens)
    word_counts = Counter(tokens)

    return word_counts, total_words


def tokenize_text(text: str) -> list[str]:
    vectorizer = TfidfVectorizer(use_idf=False, norm=None)
    analyzer = vectorizer.build_analyzer()

    return analyzer(text)


def get_document_tf(document_contents: str) -> dict[str, float] | None:
    word_counts, total_words = get_word_stats(document_contents)
    tf_dict = calculate_tf(word_counts, total_words)
    least_frequent_words = get_least_frequent_words(tf_dict)
    tf = {word: tf_dict[word] for word in least_frequent_words}

    return tf


def calculate_tf(word_counts: Counter, total_words: int) -> dict[str, float]:
    return {
        word: round(count / total_words, 3)
        for word, count in word_counts.items()
    }


def get_least_frequent_words(
    tf_dict: dict[str, float], count: int = 50
) -> list[str]:
    return [
        word for word, _ in sorted(tf_dict.items(), key=lambda x: x[1])[:count]
    ]


def calculate_idf(
    documents_in_collection: list[tuple[int, str]]
) -> dict[str, float]:
    number_of_documents = len(documents_in_collection)

    if number_of_documents == 0:
        return {}

    document_frequencies = Counter()
    for _, contents in documents_in_collection:
        words_in_document = set(tokenize_text(contents))
        document_frequencies.update(words_in_document)

    idf = {}
    for word, df in document_frequencies.items():
        idf[word] = round(math.log(number_of_documents / (1 + df)), 3)

    return idf
