import time
import sentiment_analysis
import pandas as pd
from numpy import nan
from PIL import Image
import os

bot = "{0}"
user = "USER: {0}"


def get_data(column=None):
    df_replies = pd.read_csv("Data/replies.csv")
    df_replies_selected = df_replies[column].values.tolist()
    df_replies_selected = [item for item in df_replies_selected if str(item) != 'nan']
    return df_replies_selected


def get_probing_questions():
    df_replies = pd.read_csv("Data/replies.csv")
    df_questions = df_replies['thought_record_probing_questions']
    return df_questions


def get_reply(data=None, username=None):
    reply = ""
    for i in range(len(data)):
        reply += data[i] + " "
        reply = reply.replace("USER_NAME", username)
    print(reply)
    return bot.format(reply)


def greeting(text):
    name = text
    return bot.format("Nice to meet you, " + name + "! What is bothering you right now?")


def goodbye(username=None, user_input=None):
    goodbye_replies = get_data('goodbye')
    return get_reply(goodbye_replies, username), None


