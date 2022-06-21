import matplotlib.pyplot as plt
import re
import emoji
import string
import contractions
import seaborn as sn
from nltk.tokenize import word_tokenize
# nltk.download('punkt')
from nltk.corpus import stopwords
# nltk.download('stopwords')
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
import numpy as np


# TEXT NORMALIZATION
def replace_usertag(text, default_replace="user"):
    text = re.sub('\B@\w+', default_replace, text)
    return text


def demojize(text):
    text = emoji.demojize(text)
    return text


def replace_url(text, default_replace=""):
    text = re.sub('(http|https):\/\/\S+', default_replace, text)
    return text


def replace_hashtag(text, default_replace=""):
    text = re.sub('#+', default_replace, text)
    return text


def letter_repetition(text):
    text = re.sub(r'(.)\1+', r'\1\1', text)
    return text


def punctuation_repetition(text, default_replace=""):
    text = re.sub(r'[\?\.\!]+(?=[\?\.\!])', default_replace, text)
    return text


def replace_abreviation(text):
    text = contractions.fix(text)
    return text


def tokenize(text):
    tokens = word_tokenize(text)
    return tokens


def custom_tokenize(text, keep_punctuation=False,
                    keep_alphanumerical=False, keep_stopwords=False):
    token_list = word_tokenize(text)

    if not keep_punctuation:
        token_list = [token for token in token_list if token not in string.punctuation]
    if not keep_alphanumerical:
        token_list = [token for token in token_list if token.isalpha()]

    if not keep_stopwords:
        stop_words = set(stopwords.words('english'))
        stop_words.discard("not")
        token_list = [token for token in token_list if not token in stop_words]

    return token_list


def stemming_tokens(tokens, stemmer):
    token_list = []
    for token in tokens:
        token_list.append(stemmer.stem(token))
    return token_list


def lemmatize_tokens(tokens, word_type, lemmatizer):
    token_list = []
    for token in tokens:
        token_list.append(lemmatizer.lemmatize(token, word_type[token]))
    return token_list


def process_text(text, verbose=False):
    if verbose: print("Initial tweet: {}".format(text))

    text = replace_usertag(text, "")
    text = replace_url(text)
    text = replace_hashtag(text)

    if verbose: print("Post Twitter processing tweet: {}".format(text))

    text = text.lower()
    text = replace_abreviation(text)
    text = punctuation_repetition(text)
    text = letter_repetition(text)
    text = demojize(text)

    if verbose: print("Post Word processing tweet: {}".format(text))

    tokens = custom_tokenize(text, keep_alphanumerical=False, keep_stopwords=False)
    stemmer = SnowballStemmer('english')
    stem = stemming_tokens(tokens, stemmer)

    return stem


# TEXT VECTORIZATION
def fit_tfidf(text_corpus):
    tf_vectorizer = TfidfVectorizer(preprocessor=lambda x: x, tokenizer=lambda x: x)
    tf_vectorizer.fit(text_corpus)
    return tf_vectorizer


def plot_confusion(cm):
    plt.figure(figsize=(5, 5))
    sn.heatmap(cm, annot=True, cmap="Blues", fmt='.0f')
    plt.xlabel("Prediction")
    plt.ylabel("True value")
    plt.title("Confusion Matrix")
    return sn


def linear_regression(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def build_freqs(tweet_list, sentiment_list):
    freqs = {}
    for tweet, sentiment in zip(tweet_list, sentiment_list):
        for word in tweet:
            pair = (word, sentiment)
            if pair in freqs:
                freqs[pair] += 1
            else:
                freqs[pair] = 1
    return freqs


def tweet_to_freq(tweet, freqs):
    x = np.zeros((4,))
    for word in tweet:
        if (word, 1) in freqs:
            x[0] += freqs[(word, 1)]
        if (word, 0) in freqs:
            x[0] += freqs[(word, 0)]
        if (word, 0.33) in freqs:
            x[0] += freqs[(word, 0.33)]
        if (word, 0.67) in freqs:
            x[0] += freqs[(word, 0.67)]