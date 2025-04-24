from collections import Counter

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


def process_text(text):
    vectorizer = TfidfVectorizer(use_idf=False, norm=None)
    analyzer = vectorizer.build_analyzer()
    tokens = analyzer(text)
    total_words = len(tokens)
    word_counts = Counter(tokens)
    tf_data = {
        'word': [],
        'tf': [],
        'idf': []
    }

    for word, count in word_counts.items():
        tf_data['word'].append(word)
        tf_data['tf'].append(round(count / total_words, 3))
        # log10(1/1) = 0 for all words since only 1 document is uploaded
        tf_data['idf'].append(0)

    df = pd.DataFrame(tf_data)
    df_sorted = df.sort_values(by='idf', ascending=False).head(50)

    return df_sorted
