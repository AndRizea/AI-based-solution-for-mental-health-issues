import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split
import sentiment_analysis_functions as function

# LOAD AND ANALYZE THE DATASET
df_dataset = pd.read_csv("Data/all_data.txt", sep="	", header=None)
df_dataset.columns = ["id", "tweet_text", "sentiment", "threshold"]

# distribution of sentiments in the training dataset
sentiment_count = df_dataset["sentiment"].value_counts()
print(sentiment_count)
plt.pie(sentiment_count, labels=sentiment_count.index,
        autopct='%1.1f%%', shadow=True, startangle=140)
plt.title("Distribution of sentiments in the training dataset")
plt.show()

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
plt.show()

pos_tweets = df_dataset[df_dataset["sentiment"] == "fear"]
txt = " ".join(tweet.lower() for tweet in pos_tweets["tweet_text"])
wordcloud = WordCloud().generate(txt)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Words used often to describe fear")
plt.show()

pos_tweets = df_dataset[df_dataset["sentiment"] == "joy"]
txt = " ".join(tweet.lower() for tweet in pos_tweets["tweet_text"])
wordcloud = WordCloud().generate(txt)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Words used often to describe joy")
plt.show()

pos_tweets = df_dataset[df_dataset["sentiment"] == "sadness"]
txt = " ".join(tweet.lower() for tweet in pos_tweets["tweet_text"])
wordcloud = WordCloud().generate(txt)
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.title("Words used often to describe sadness")
plt.show()

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

print("Size of X_train: {}".format(len(X_train)))
print("Size of y_train: {}".format(len(y_train)))
print("\n")
print("Size of X_test: {}".format(len(X_test)))
print("Size of y_test: {}".format(len(y_test)))
print("\n")
print("Train proportion: {:.0%}".format(len(X_train) / (len(X_train) + len(X_test))))

tf_idf = function.fit_tfidf(X_train)
X_train_tf = tf_idf.transform(X_train)
X_test_tf = tf_idf.transform(X_test)
final_model = function.logistic_regression(X_train_tf, y_train)

user_text = "The war in Ukraine is getting more and more deadly, I wish I could help more people 🙁"

forms_data = pd.read_csv("Data/Artificial Intelligence (AI) Based Solution for Mental Health Issues.csv")
forms_data_sadness = forms_data["Say something that may express sadness"]
forms_data_fear = forms_data["Say something that may express fear"]
forms_data_anger = forms_data["Say something that may express anger"]
forms_data_joy = forms_data["Say something that may express joy"]

#print(forms_data_sadness)

def predict_text(text):
    processed_text = function.process_text(text)
    transformed_text = tf_idf.transform([processed_text])
    prediction = final_model.predict(transformed_text)
    #print(prediction)

    if prediction >= 1:
        message = "Prediction is: joy"
    else:
        if (prediction >= 0.67) and (prediction < 1):
            message = "Prediction is: anger"
        else:
            if (prediction >= 0.33) and (prediction < 0.67):
                message = "Prediction is: fear"
            else:
                if prediction < 0.33:
                    message = "Prediction is: sadness"

    return prediction, message


# print("-------------------------IT SHOULD BE SADNESS-----------------------------")
# predict_fear_instead_of_sadness = 0
# predict_anger_instead_of_sadness = 0
# predict_joy_instead_of_sadness = 0
# ok = 0
# for i in range(0, len(forms_data_sadness)):
#     prediction_score = 0
#     print("User message: {}".format(forms_data_sadness[i]))
#     predict_text(forms_data_sadness[i])
#     prediction_score, prediction_text = predict_text(forms_data_sadness[i])
#     print("Score: {}".format(prediction_score))
#     print("Prediction: {}".format(prediction_text))
#     print("\n")
#     if prediction_text == "Prediction is: fear":
#         predict_fear_instead_of_sadness += 1
#     else:
#         if prediction_text == "Prediction is: anger":
#             predict_anger_instead_of_sadness += 1
#         else:
#             if prediction_text == "Prediction is: joy":
#                 predict_joy_instead_of_sadness += 1
#             else:
#                 ok += 1
#
# print("-----------------------")
# print("predict_fear_instead_of_sadness: ", predict_fear_instead_of_sadness)
# print("predict_anger_instead_of_sadness: ", predict_anger_instead_of_sadness)
# print("predict_joy_instead_of_sadness: ", predict_joy_instead_of_sadness)
# print("ok: ", ok)
#
# print("-------------------------IT SHOULD BE FEAR-----------------------------")
# predict_sadness_instead_of_fear = 0
# predict_anger_instead_of_fear = 0
# predict_joy_instead_of_fear = 0
# ok = 0
# for i in range(0, len(forms_data_fear)):
#     print("User message: {}".format(forms_data_fear[i]))
#     predict_text(forms_data_fear[i])
#     prediction_score, prediction_text = predict_text(forms_data_fear[i])
#     print("Score: {}".format(prediction_score))
#     print("Prediction: {}".format(prediction_text))
#     print("\n")
#     if prediction_text == "Prediction is: sadness":
#         predict_sadness_instead_of_fear += 1
#     else:
#         if prediction_text == "Prediction is: anger":
#             predict_anger_instead_of_fear += 1
#         else:
#             if prediction_text == "Prediction is: joy":
#                 predict_joy_instead_of_fear += 1
#             else:
#                 ok += 1
#
# print("-----------------------")
# print("predict_sadness_instead_of_fear: ", predict_sadness_instead_of_fear)
# print("predict_anger_instead_of_fear: ", predict_anger_instead_of_fear)
# print("predict_joy_instead_of_fear: ", predict_joy_instead_of_fear)
# print("ok: ", ok)
#
# print("-------------------------IT SHOULD BE ANGER-----------------------------")
# predict_sadness_instead_of_anger = 0
# predict_fear_instead_of_anger = 0
# predict_joy_instead_of_anger = 0
# ok = 0
# for i in range(0, len(forms_data_anger)):
#     print("User message: {}".format(forms_data_anger[i]))
#     predict_text(forms_data_anger[i])
#     prediction_score, prediction_text = predict_text(forms_data_anger[i])
#     print("Score: {}".format(prediction_score))
#     print("Prediction: {}".format(prediction_text))
#     print("\n")
#     if prediction_text == "Prediction is: fear":
#         predict_fear_instead_of_anger += 1
#     else:
#         if prediction_text == "Prediction is: sadness":
#             predict_sadness_instead_of_anger += 1
#         else:
#             if prediction_text == "Prediction is: joy":
#                 predict_joy_instead_of_anger += 1
#             else:
#                 ok += 1
#
# print("-----------------------")
# print("predict_sadness_instead_of_anger: ", predict_sadness_instead_of_anger)
# print("predict_fear_instead_of_anger: ", predict_fear_instead_of_anger)
# print("predict_joy_instead_of_anger: ", predict_joy_instead_of_anger)
# print("ok: ", ok)
#
# print("-------------------------IT SHOULD BE JOY-----------------------------")
# predict_sadness_instead_of_joy = 0
# predict_anger_instead_of_joy = 0
# predict_fear_instead_of_joy = 0
# ok = 0
# for i in range(0, len(forms_data_joy)):
#     print("User message: {}".format(forms_data_joy[i]))
#     predict_text(forms_data_joy[i])
#     preidiction_score, prediction_text = predict_text(forms_data_joy[i])
#     print("Score: {}".format(prediction_score))
#     print("Prediction: {}".format(prediction_text))
#     print("\n")
#     if prediction_text == "Prediction is: fear":
#         predict_fear_instead_of_joy += 1
#     else:
#         if prediction_text == "Prediction is: anger":
#             predict_anger_instead_of_joy += 1
#         else:
#             if prediction_text == "Prediction is: sadness":
#                 predict_sadness_instead_of_joy += 1
#             else:
#                 ok += 1
#
# print("-----------------------")
# print("predict_sadness_instead_of_joy: ", predict_sadness_instead_of_joy)
# print("predict_fear_instead_of_joy: ", predict_fear_instead_of_joy)
# print("predict_anger_instead_of_joy: ", predict_anger_instead_of_joy)
# print("ok: ", ok)
#
# msg = "I don't feel like going out tonight because I just found out that my grandpa has a very rare illness and now he is hospitalized"
# score, text = predict_text(msg)
# print("Score: ", score, text)