import time
import pandas as pd
from numpy import nan
from PIL import Image

bot = "CloudBot ☁: {0}"
user = "USER: {0}"


def get_data(column=None):
    df_replies = pd.read_csv("Data/replies.csv")
    df_replies_selected = df_replies[column].values.tolist()
    df_replies_selected = [item for item in df_replies_selected if str(item) != 'nan']
    return df_replies_selected


def get_reply(username, data=None, time_sleep=None):
    for i in range(len(data)):
        reply = data[i]
        reply = reply.replace("USER_NAME", username)
        print(bot.format(reply))
        time.sleep(time_sleep)


def greeting():
    intro_replies = get_data('intro')
    #get_reply(intro_replies, 3)
    for i in range(len(intro_replies)):
        reply = intro_replies[i]
        print(bot.format(reply))
        time.sleep(3)
    name = input()
    time.sleep(1)
    print(bot.format("Nice to meet you, " + name + "! ☁"))
    return name


def goodbye(username):
    goodbye_replies = get_data('goodbye')
    get_reply(username, goodbye_replies, 2)


def recommend_supervised_help():
    recommend_replies = get_data('recommend_supervised_help')
    get_reply(recommend_replies, 2)


def suggestions(column, time_sleep):
    df_replies = pd.read_csv("Data/suggestions.csv")
    df_replies_selected = df_replies[column].values.tolist()
    df_replies_selected = [item for item in df_replies_selected if str(item) != 'nan']
    for i in range(len(df_replies_selected)):
        reply = df_replies_selected[i]
        print(bot.format(reply))
        time.sleep(time_sleep)



