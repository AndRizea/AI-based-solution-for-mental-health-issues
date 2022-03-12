import nltk
import numpy as np
from nltk.stem.lancaster import LancasterStemmer



# Textual sentiment analysis
anger_training_set = []
fear_training_set = []
sadness_training_set = []
happiness_training_set = []

anger_test_set = []
fear_test_set = []
sadness_test_set = []
happiness_test_set = []

def load_training_data(sentiment):
    data = open("../Data/" + sentiment + "_training_set.txt", encoding="utf8")
    if sentiment == "anger":
        threshold = 0.5
    elif sentiment == "fear":
        threshold = 0.5
    elif sentiment == "sadness":
        threshold = 0.5
    elif sentiment == "happiness":
        threshold = 0.5

    return data, threshold

def load_test_data(sentiment):
    data = open("../Data/" + sentiment + "_training_set.txt", encoding="utf8")
    return data

def clean_data(training_data, threshold):
    trained_set = []
    for line in training_data:
        line = line.strip().lower
        if line.split()[-1] == "none":
            line = " ".join(filter(lambda x: x[0] != '@', line.split()))
            punctuation = line.maketrans("", "", '.*%$^0123456789#!][\?&/)/(+-<>')
            result = line.translate(punctuation)
            tokened_sentence = nltk.word_tokenize(result)
            sentence = tokened_sentence[0:len(tokened_sentence) - 1]
            label = tokened_sentence[-2]
            trained_set.append((sentence, label))
        else:
            intensity = float(line.split()[-1])
            if(intensity >= threshold):
                line = " ".join(filter(lambda x: x[0] != '@', line.split()))
                punctuation = line.maketrans("", "", '.*%$^0123456789#!][\?&/)/(+-<>')
                result = line.translate(punctuation)
                tokened_sentence = nltk.word_tokenize(result)
                sentence = tokened_sentence[0:len(tokened_sentence) - 1]
                label = tokened_sentence[-1]
                trained_set.append((sentence, label))
    return trained_set


# Build the chatbot

