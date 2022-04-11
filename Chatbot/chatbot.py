import time
import chatbot_functions as chatbot_function
import exercises
import sentiment_analysis
import pandas as pd
from numpy import nan
from PIL import Image

bot = "CloudBot ☁: {0}"
user = "USER: {0}"

def identify_sentiment():
    time.sleep(1)
    print(bot.format(name + ", what is bothering you right now?"))
    response = input()
    prediction, _ = sentiment_analysis.predict_text(response)
    return prediction

def sadness():
    time.sleep(1)
    print(bot.format(name + ", I am sorry to hear that..."))
    time.sleep(2)
    sadness_replies = chatbot_function.get_data('handle_sadness')
    chatbot_function.get_reply(sadness_replies, 3)
    print(bot.format("What usually helps you feel better in this situation, " + name + "?")) # to do: scenariu pt cand spune "nu stiu"
    feel_better_action = input()
    time.sleep(1)
    print(bot.format("I see. Do you think there is a way in which you could achieve this right now?"))
    time.sleep(1)
    print(bot.format("PLease respond by yes or no"))
    response = input()
    # im = Image.open("Data/feelings process.png")
    # im.show()
    if response.lower() == "yes":
        print(bot.format("This sounds good!✨"))
        time.sleep(1)
        print(bot.format("Would you want to tell me more about it?"))
        response = input()
        if response == 'no':
            print(bot.format("Amazing! " + feel_better_action + " sounds great"))
            time.sleep(2)
            chatbot_function.goodbye()
        if response == 'yes':
            print(bot.format("Alright, this is amazing! Go ahead!"))
            input()
            time.sleep(1)
            print(bot.format("Amazing! " + feel_better_action + " sounds great"))
            time.sleep(2)
            print(bot.format("For the moment, what would you like to add to our conversation?"))
            input()
            time.sleep(1)
            print(bot.format("Alright then!"))
            time.sleep(1)
            chatbot_function.goodbye()
        time.sleep(1)
    elif response.lower() == "no":
        print(bot.format("It's alright, don't get scared. In the next moments, we will find other solutions in order to make you feel better ❤"))
        exercises.thought_record(user_name=name)


name = chatbot_function.greeting()
prediction = identify_sentiment()

if prediction < 0.33:
    sadness()
else:
    print(bot.format("Sorry, but for the moment I can't understand what are you really feeling. I will get better in the following period, I promise!"))
    print(bot.format("Until then, stay strong!"))