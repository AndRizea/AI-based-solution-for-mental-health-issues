import pandas as pd
import numpy
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import emoji
import string
import contractions
import random
import nltk
from nltk.tokenize import word_tokenize
#nltk.download('punkt')
from nltk.corpus import stopwords
#nltk.download('stopwords')
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
#nltk.download('wordnet')
from sklearn.feature_extraction.text import TfidfVectorizer

#LOAD AND ANALYZE THE DATASET
df_all = pd.read_csv("Data/all_training_data.txt", sep="	", header=None)
df_all.columns = ["id", "tweet_text", "sentiment", "threshold"]

# distribution of sentiments in the dataset
sentiment_count = df_all["sentiment"].value_counts()
plt.pie(sentiment_count, labels=sentiment_count.index,
        autopct='%1.1f%%', shadow=True, startangle=140)
#plt.show()

df_training_anger = df_all[df_all["sentiment"] == "anger"]
df_training_fear = df_all[df_all["sentiment"] == "fear"]
df_training_joy = df_all[df_all["sentiment"] == "joy"]
df_training_sadness = df_all[df_all["sentiment"] == "sadness"]

#WordClouds - What are the words most often present in expressing a certain type of emotion?
pos_tweets = df_all[df_all["sentiment"] == "anger"]
txt = " ".join(tweet.lower() for tweet in pos_tweets["tweet_text"])
wordcloud = WordCloud().generate(txt)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Words used often to describe anger")
#plt.show()

pos_tweets = df_all[df_all["sentiment"] == "fear"]
txt = " ".join(tweet.lower() for tweet in pos_tweets["tweet_text"])
wordcloud = WordCloud().generate(txt)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Words used often to describe fear")
#plt.show()

pos_tweets = df_all[df_all["sentiment"] == "joy"]
txt = " ".join(tweet.lower() for tweet in pos_tweets["tweet_text"])
wordcloud = WordCloud().generate(txt)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Words used often to describe joy")
#plt.show()

pos_tweets = df_all[df_all["sentiment"] == "sadness"]
txt = " ".join(tweet.lower() for tweet in pos_tweets["tweet_text"])
wordcloud = WordCloud().generate(txt)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Words used often to describe sadness")
#plt.show()

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

snowball_stemmer = SnowballStemmer('english')
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

# TEXT REPRESENTATION
df_all["tokens"] = df_all["tweet_text"].apply(process_text)
df_all["sentiment_score"] = df_all["sentiment"].apply(lambda i: 1 if i == "joy" else (0.75 if i == "anger" else (0.5 if i == "fear" else 0)))
#print(df_all.head(10))
#df_all.to_csv("Data/all_training_data.csv")

X = df_all["tokens"].tolist()
y = df_all["sentiment_score"].tolist()

#TF-IDF
def fit_tfidf(text_corpus):
        tf_vectorizer = TfidfVectorizer(preprocessor=lambda x: x, tokenizer=lambda x: x)
        tf_vectorizer.fit(text_corpus)
        return tf_vectorizer

