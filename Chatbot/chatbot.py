import time
import sentiment_analysis

bot = "CloudBot ☁: {0}"
user = "USER: {0}"

def greeting():
    print(bot.format("Hi, I'm CloudBot 😊"))
    time.sleep(2)
    print(bot.format("Let me introduce myself. I am a trained medical bot used mostly for managing mental health "
                     "issues using Cognitive Behavioral Therapy (CBT) techniques."))
    time.sleep(4)
    print(bot.format("If you want to learn more about these techniques, I encourage you to visit the link below "))
    print(bot.format("https://cogbtherapy.com/cognitive-behavior-therapy-techniques"))
    time.sleep(3)
    print(bot.format("I am here to help you whenever you may feel down or you may need somebody to talk to."))
    time.sleep(3)
    print(bot.format("Now, what about you? What's your name?"))
    name = input()
    time.sleep(1)
    print(bot.format("Nice to meet you, " + name))
    return name

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
    print(bot.format("I am here for you. Together we can pass over it, ok?"))
    time.sleep(2)
    print(bot.format("I assume that this feeling can impact your daily activities 🥺"))
    time.sleep(2)
    print(bot.format("But listen, everything that you need to cope with this sentiment is within you."))
    time.sleep(3)
    print(bot.format("What usually helps you feel better in this situation, " + name + "?")) # to do: scenariu pt cand spune "nu stiu"
    input()
    time.sleep(1)
    print(bot.format("I see. Do you think that is there a way in which you could achieve this right now?"))
    time.sleep(1)
    print(bot.format("PLease respond by yes or no"))
    response = input()
    if response.lower() == "yes":
        print(bot.format("This sounds good!✨"))
        time.sleep(1)
        print(bot.format("Would you want to tell me more about it?"))
        input()
        time.sleep(1)
        print(bot.format("Alright, this is amazing!"))
    elif response.lower() == "no":
        print(bot.format("It's alright, don't get scared. In the next moments, we will find other solutions in order to make you feel better ❤"))

name = greeting()
prediction = identify_sentiment()

if prediction < 0.33:
    sadness()
else:
    print(bot.format("Sorry, but for the moment I can't understand what are you really feeling. I will get better in the following period, I promise!"))
    print(bot.format("Until then, stay strong!"))