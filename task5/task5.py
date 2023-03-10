import os
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer
from sklearn.feature_extraction.text import CountVectorizer
import string
import warnings
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity
warnings.filterwarnings("ignore")

DATA_PATH = 'D:/khovaev/programs/ideaProjects/Pycharm/infopoisk/data'
TOKENS_PATH = 'D:/khovaev/programs/ideaProjects/Pycharm/infopoisk/tokens'
LEMMAS_PATH = 'D:/khovaev/programs/ideaProjects/Pycharm/infopoisk/lemmas/lemmas'
WORDS_INDEX_PATH = 'D:/khovaev/programs/ideaProjects/Pycharm/infopoisk/src/task3/words_index.txt'

vectors = {}
all_lemmas = []
files = os.listdir(LEMMAS_PATH)
cos_distance = {}

total = set(str(i) for i in range(len(files)))
noise = stopwords.words('russian') + list(string.punctuation)


def get_all_lemmas():
    for i in range(len(files)):
        with open(f'{LEMMAS_PATH}/{i}.txt', 'r', encoding='utf-8') as file:
            while True:
                line = file.readline()[:-1]
                if not line:
                    break
                elif line not in all_lemmas:
                    all_lemmas.append(line)


def word_tokenization(t):
    vectorized = CountVectorizer(ngram_range=(1, 1),
                                 tokenizer=word_tokenize,
                                 stop_words=noise)

    vectorized.fit_transform(t)
    return list(vectorized.vocabulary_)


if __name__ == "__main__":
    get_all_lemmas()
    for i in range(len(files)):
        file_words = []
        with open(f'{LEMMAS_PATH}/{i}.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()[:-1]
        vectors[i] = []
        lines = [i[:-1] for i in lines]
        for j in all_lemmas:
            if j in lines:
                vectors[i].append(1)
            else:
                vectors[i].append(0)
    print('input:')
    words = input()
    words = re.sub(r'[^а-я]', " ", words.lower())
    tokens = word_tokenization([words])

    pymorphy2_analyzer = MorphAnalyzer()
    normal_form = []
    for j in tokens:
        ana = pymorphy2_analyzer.parse(j)
        normal_form.append(ana[0].normal_form)
    indexing = []
    for i in all_lemmas:
        if i in normal_form:
            indexing.append(1)
        else:
            indexing.append(0)

    if 1 in indexing:
        for k, v in vectors.items():
            cos_distance[k] = spatial.distance.cosine(v, indexing)

        sorted_keys = sorted(cos_distance, key=cos_distance.get, reverse=True)

        for v in sorted_keys:
            print(f'{v}: {cos_distance[v]}')
    else:
        print('Введённые слова не были найдены в словаре')
