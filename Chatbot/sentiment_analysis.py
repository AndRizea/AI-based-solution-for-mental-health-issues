import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import re
import emoji
import string
import contractions
import seaborn as sn
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
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

#LOAD AND ANALYZE THE DATASET
df_dataset = pd.read_csv("Data/all_data.txt", sep="	", header=None)
df_dataset.columns = ["id", "tweet_text", "sentiment", "threshold"]

# distribution of sentiments in the training dataset
sentiment_count = df_dataset["sentiment"].value_counts()
plt.pie(sentiment_count, labels=sentiment_count.index,
        autopct='%1.1f%%', shadow=True, startangle=140)
plt.title("Distribution of sentiments in the training dataset")
#plt.show()

df_training_anger = df_dataset[df_dataset["sentiment"] == "anger"]
df_training_fear = df_dataset[df_dataset["sentiment"] == "fear"]
df_training_joy = df_dataset[df_dataset["sentiment"] == "joy"]
df_training_sadness = df_dataset[df_dataset["sentiment"] == "sadness"]

#WordClouds - What are the words most often present in expressing a certain type of emotion?
pos_tweets = df_dataset[df_dataset["sentiment"] == "anger"]
txt = " ".join(tweet.lower() for tweet in pos_tweets["tweet_text"])
wordcloud = WordCloud().generate(txt)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Words used often to describe anger")
#plt.show()

pos_tweets = df_dataset[df_dataset["sentiment"] == "fear"]
txt = " ".join(tweet.lower() for tweet in pos_tweets["tweet_text"])
wordcloud = WordCloud().generate(txt)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Words used often to describe fear")
#plt.show()

pos_tweets = df_dataset[df_dataset["sentiment"] == "joy"]
txt = " ".join(tweet.lower() for tweet in pos_tweets["tweet_text"])
wordcloud = WordCloud().generate(txt)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Words used often to describe joy")
#plt.show()

pos_tweets = df_dataset[df_dataset["sentiment"] == "sadness"]
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

# TEXT VECTORIZATION
df_dataset["tokens"] = df_dataset["tweet_text"].apply(process_text)
df_dataset["sentiment_score"] = df_dataset["sentiment"].apply(lambda i: 1 if i == "joy" else (0.67 if i == "anger" else (0.33 if i == "fear" else 0)))
#print(df_all.head(10))
#df_all.to_csv("Data/all_training_data.csv")

X= df_dataset["tokens"].tolist()
y = df_dataset["sentiment_score"].tolist()


#TF-IDF
def fit_tfidf(text_corpus):
        tf_vectorizer = TfidfVectorizer(preprocessor=lambda x: x, tokenizer=lambda x: x)
        tf_vectorizer.fit(text_corpus)
        return tf_vectorizer

#SENTIMENT ANALYSIS
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    random_state=0,
                                                    train_size=0.80)

#y_test = np.asarray(y_test)
#y_test = y_test.astype('float')
#print(y_train)
#y_train = y_train.astype('float32')
#print(type(y_train))
#print(type(y_train[7]))

#print("Size of X_train: {}".format(len(X_train)))
#print("Size of y_train: {}".format(len(y_train)))
#print("\n")
#print("Size of X_test: {}".format(len(X_test)))
#print("Size of y_test: {}".format(len(y_test)))
#print("\n")
#print("Train proportion: {:.0%}".format(len(X_train) / (len(X_train) + len(X_test))))

def plot_confusion(cm):
        plt.figure(figsize = (5,5))
        sn.heatmap(cm, annot=True, cmap="Blues", fmt='.0f')
        plt.xlabel("Prediction")
        plt.ylabel("True value")
        plt.title("Confusion Matrix")
        return sn

def logistic_regression(X_train, y_train):
        model = LinearRegression()
        model.fit(X_train, y_train)
        return model

tf_idf = fit_tfidf(X_train)
X_train_tf = tf_idf.transform(X_train)
X_test_tf = tf_idf.transform(X_test)
final_model= logistic_regression(X_train_tf, y_train)


user_text = "Turn off the light when you leave the room!"
def predict_text(text):
        processed_text = process_text(text)
        transformed_text = tf_idf.transform([processed_text])
        prediction = final_model.predict(transformed_text)
        print(prediction)

        if prediction >= 1:
                print("Prediction is: joy")
        else:
                if ((prediction >= 0.67) and (prediction < 1)):
                        print("Prediction is: anger")
                else:
                        if ((prediction >= 0.33) and (prediction < 0.67)):
                                print("Prediction is: fear")
                        else:
                                if prediction < 0.33:
                                        print("Prediction is: sadness")


print("User message: {}".format(user_text))
predict_text(user_text)