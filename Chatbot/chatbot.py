import nltk
import numpy as np
from nltk.stem.lancaster import LancasterStemmer



# Textual sentiment analysis
stemmer = LancasterStemmer()

def load_training_data(sentiment):
    data = open("Data/" + sentiment + "_training_set.txt", encoding="utf8")
    threshold = 0
    if sentiment == "anger":
        threshold = 0.5
    elif sentiment == "fear":
        threshold = 0.6
    elif sentiment == "sadness":
        threshold = 0.5
    elif sentiment == "happiness":
        threshold = 0.5

    return data, threshold

def load_test_data(sentiment):
    data = open("Data/" + sentiment + "_training_set.txt", encoding="utf8")
    return data

def clean_data(training_data, threshold):
    training_set = []
    for line in training_data:
        line = line.strip().lower() #strip() - remove spaces at the beginning and at the end of the string
        if line.split()[-1] == "none": #last word in the line
            line = " ".join(filter(lambda x: x[0] != '@', line.split()))
            punctuation = line.maketrans("", "", '.*%$^0123456789#!][\?&/)/(+-<>')
            result = line.translate(punctuation)
            tokened_sentence = nltk.word_tokenize(result)
            sentence = tokened_sentence[0:len(tokened_sentence) - 1]
            label = tokened_sentence[-2]
            training_set.append((sentence, label))
        else:
            intensity = float(line.split()[-1])
            if(intensity >= threshold):
                line = " ".join(filter(lambda x: x[0] != '@', line.split()))
                punctuation = line.maketrans("", "", '.*%$^0123456789#!][\?&/)/(+-<>')
                result = line.translate(punctuation)
                tokened_sentence = nltk.word_tokenize(result)
                sentence = tokened_sentence[0:len(tokened_sentence) - 1]
                label = tokened_sentence[-1]
                training_set.append((sentence, label))
    return training_set

def encode_sentence(all_words, sentence, bag):
    for sentence_word in sentence:
        stemmed_word = stemmer.stem(sentence_word)
        for i, word in enumerate(all_words):
            if stemmed_word == word:
                bag[i] = 1
    return bag

def bag_of_words(data):
    training_set = []
    all_words = []
    for list in data:
        for words in list[0]:
            word = stemmer.stem(words)
            all_words.append(word)

    all_words = list(set(all_words))

    for sentence in data:
        bag = [0] * len(all_words)
        training_set.append(encode_sentence(all_words, sentence[0], bag))

    return training_set, all_words


load_anger_training_data, threshold = load_training_data("anger")
print("***************************Loading data for anger**************************")
anger_training_set = clean_data(load_anger_training_data, threshold)
print(len(anger_training_set))

load_fear_training_data, threshold = load_training_data("fear")
print("***************************Loading data for fear**************************")
fear_training_set = clean_data(load_fear_training_data, threshold)

load_sadness_training_data, threshold = load_training_data("sadness")
print("***************************Loading data for sadness**************************")
sadness_training_set = clean_data(load_sadness_training_data, threshold)

load_joy_training_data, threshold = load_training_data("joy")
print("***************************Loading data for joy**************************")
joy_training_set = clean_data(load_joy_training_data, threshold)

load_anger_test_data = load_test_data("anger")
anger_test_data = clean_data(load_anger_test_data, threshold)

load_fear_test_data = load_test_data("fear")
fear_test_data = clean_data(load_fear_test_data, threshold)

load_sadness_test_data = load_test_data("sadness")
sadness_test_data = clean_data(load_sadness_test_data, threshold)

load_joy_test_data = load_test_data("joy")
joy_test_data = clean_data(load_joy_test_data, threshold)



# Build the chatbot

