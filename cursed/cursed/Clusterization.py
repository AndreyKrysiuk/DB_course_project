import sys
import cursed.settings
import numpy as np

import re
from Stemmer import Stemmer
from cursed import NewsModel
from cursed import ClusterElementModel
import matplotlib.pyplot as plt
from matplotlib import cm


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.pipeline import Pipeline

def text_cleaner(text):
    text = text.lower()  # приведение в lowercase,

    text = re.sub(r'https?://[\S]+', ' url ', text)  # замена интернет ссылок
    text = re.sub(r'[\w\./]+\.[a-z]+', ' url ', text)

    text = re.sub(r'\d+[-/\.]\d+[-/\.]\d+', ' date ', text)  # замена даты и времени
    text = re.sub(r'\d+ ?гг?', ' date ', text)
    text = re.sub(r'\d+:\d+(:\d+)?', ' time ', text)

    # text = re.sub( r'@\w+', ' tname ', text ) # замена имён twiter
    # text = re.sub( r'#\w+', ' htag ', text ) # замена хештегов

    text = re.sub(r'<[^>]*>', ' ', text)  # удаление html тагов
    text = re.sub(r'[\W]+', ' ', text)  # удаление лишних символов

    stemmer = Stemmer('russian')
    text = ' '.join(stemmer.stemWords(text.split()))

    stw = ['в', 'по', 'на', 'из', 'и', 'или', 'не', 'но', 'за', 'над', 'под', 'то',
           'a', 'at', 'on', 'of', 'and', 'or', 'in', 'for', 'at']
    remove = r'\b(' + '|'.join(stw) + ')\b'
    text = re.sub(remove, ' ', text)

    text = re.sub(r'\b\w\b', ' ', text)  # удаление отдельно стоящих букв

    text = re.sub(r'\b\d+\b', ' digit ', text)  # замена цифр

    return text


def save2db(data, clusters):
    for i in range(0, len(data)):
        ClusterElementModel.add_cluster(data[i].title, clusters[i])


def main():
    print("[i] загружаем данные...")
    data = NewsModel.get_news()

    print("[i] очистка данных...")
    D = [text_cleaner(t.title + "\n" + t.text) for t in data]

    n_clusters = 2000
    print("[i] начинаем разбор")
    text_clstz = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('km', KMeans(n_clusters=n_clusters)),
        # ( 'km', KMeans(n_clusters=n_clusters, init='random', n_init=10, max_iter=300, tol=1e-04, random_state=0) )
    ])

    text_clstz.fit(D)

    clusters = text_clstz.predict(D)
    print("[i] сохраняем результат...")

    save2db(data, clusters)






