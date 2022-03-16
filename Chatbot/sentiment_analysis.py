import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split
import functions as function

# LOAD AND ANALYZE THE DATASET
df_dataset = pd.read_csv("Data/all_data.txt", sep="	", header=None)
df_dataset.columns = ["id", "tweet_text", "sentiment", "threshold"]

# distribution of sentiments in the training dataset
sentiment_count = df_dataset["sentiment"].value_counts()
plt.pie(sentiment_count, labels=sentiment_count.index,
        autopct='%1.1f%%', shadow=True, startangle=140)
plt.title("Distribution of sentiments in the training dataset")
# plt.show()

df_training_anger = df_dataset[df_dataset["sentiment"] == "anger"]
df_training_fear = df_dataset[df_dataset["sentiment"] == "fear"]
df_training_joy = df_dataset[df_dataset["sentiment"] == "joy"]
df_training_sadness = df_dataset[df_dataset["sentiment"] == "sadness"]

# WordClouds - What are the words most often present in expressing a certain type of emotion?
pos_tweets = df_dataset[df_dataset["sentiment"] == "anger"]
txt = " ".join(tweet.lower() for tweet in pos_tweets["tweet_text"])
wordcloud = WordCloud().generate(txt)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Words used often to describe anger")
# plt.show()

pos_tweets = df_dataset[df_dataset["sentiment"] == "fear"]
txt = " ".join(tweet.lower() for tweet in pos_tweets["tweet_text"])
wordcloud = WordCloud().generate(txt)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Words used often to describe fear")
# plt.show()

pos_tweets = df_dataset[df_dataset["sentiment"] == "joy"]
txt = " ".join(tweet.lower() for tweet in pos_tweets["tweet_text"])
wordcloud = WordCloud().generate(txt)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Words used often to describe joy")
# plt.show()

pos_tweets = df_dataset[df_dataset["sentiment"] == "sadness"]
txt = " ".join(tweet.lower() for tweet in pos_tweets["tweet_text"])
wordcloud = WordCloud().generate(txt)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Words used often to describe sadness")
# plt.show()

# TEXT NORMALIZATION
snowball_stemmer = SnowballStemmer('english')

# TEXT VECTORIZATION
df_dataset["tokens"] = df_dataset["tweet_text"].apply(function.process_text)
df_dataset["sentiment_score"] = df_dataset["sentiment"].apply(
    lambda i: 1 if i == "joy" else (0.67 if i == "anger" else (0.33 if i == "fear" else 0)))
# print(df_all.head(10))
# df_all.to_csv("Data/all_training_data.csv")

X = df_dataset["tokens"].tolist()
y = df_dataset["sentiment_score"].tolist()

# SENTIMENT ANALYSIS
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    random_state=0,
                                                    train_size=0.80)

# print("Size of X_train: {}".format(len(X_train)))
# print("Size of y_train: {}".format(len(y_train)))
# print("\n")
# print("Size of X_test: {}".format(len(X_test)))
# print("Size of y_test: {}".format(len(y_test)))
# print("\n")
# print("Train proportion: {:.0%}".format(len(X_train) / (len(X_train) + len(X_test))))

tf_idf = function.fit_tfidf(X_train)
X_train_tf = tf_idf.transform(X_train)
X_test_tf = tf_idf.transform(X_test)
final_model = function.logistic_regression(X_train_tf, y_train)

user_text = "i am terrified of heights"


def predict_text(text):
    processed_text = function.process_text(text)
    transformed_text = tf_idf.transform([processed_text])
    prediction = final_model.predict(transformed_text)
    print(prediction)

    if prediction >= 1:
        print("Prediction is: joy")
    else:
        if (prediction >= 0.67) and (prediction < 1):
            print("Prediction is: anger")
        else:
            if (prediction >= 0.33) and (prediction < 0.67):
                print("Prediction is: fear")
            else:
                if prediction < 0.33:
                    print("Prediction is: sadness")


print("User message: {}".format(user_text))
predict_text(user_text)
