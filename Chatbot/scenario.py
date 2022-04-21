import chatbot_functions as chatbot_function
import time
import exercises

bot = "CloudBot ☁: {0}"


def sadness(user_name):
    time.sleep(1)
    print(bot.format(user_name + ", I am sorry to hear that..."))
    time.sleep(2)
    sadness_replies = chatbot_function.get_data('handle_sadness')
    chatbot_function.get_reply(username=user_name, data=sadness_replies, time_sleep=3)
    print(bot.format("What usually helps you feel better in this situation, " + user_name + "?"))
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
        time.sleep(1)
    elif response.lower() == "no":
        print(bot.format("It's alright, don't get scared. In the next moments, we will find other solutions in order to make you feel better ❤"))
        exercises.thought_record(user_name=user_name)
