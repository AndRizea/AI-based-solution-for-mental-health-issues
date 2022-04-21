import time
import chatbot_functions as chatbot_function
import sentiment_analysis
import scenario

bot = "CloudBot ☁: {0}"
user = "USER: {0}"

def identify_sentiment():
    time.sleep(1)
    print(bot.format(name + ", what is bothering you right now?"))
    response = input()
    prediction, _ = sentiment_analysis.predict_text(response)
    return prediction


name = chatbot_function.greeting()
prediction = identify_sentiment()

if prediction < 0.33:
    scenario.sadness(name)
    print(bot.format(name + " , before you go, would you like to take a look over some podcasts that you may find useful?"))
    time.sleep(1)
    print(bot.format("PLease respond by yes or no"))
    response = input()
    if response.lower() == "yes":
        chatbot_function.suggestions(column="sadness", time_sleep=2)
        chatbot_function.goodbye()
    else:
        chatbot_function.goodbye()
else:
    print(bot.format("Sorry, but for the moment I can't understand what are you really feeling. I will get better in the following period, I promise!"))
    print(bot.format("Until then, stay strong!"))
