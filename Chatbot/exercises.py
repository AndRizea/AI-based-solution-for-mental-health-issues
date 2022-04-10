import chatbot_functions as chatbot_function
import pandas as pd
import time
import sentiment_analysis

bot = "CloudBot ☁: {0}"
user = "USER: {0}"

def thought_record(user_name):
    thought_record_replies = chatbot_function.get_data('thought_record_intro')
    chatbot_function.get_reply(thought_record_replies, 3)
    print(bot.format("Now I will let you do the steps from 1 to 3 for the next 3 minutes."))
    time.sleep(2)
    print(bot.format("I can let to think more than 3 minutes, so take your time and reflect ✨"))
    time.sleep(2)
    print(bot.format("I know that this activity can be emotionally consuming, so just type READY when you finish 😊"))
    ready = input()
    if ready.lower() == 'ready':
        print(bot.format("Ok, " + user_name + ", now that you completed the steps from 1 to 3, let's move forward! ✨"))
        time.sleep(3)
        print(bot.format("Please pick one automatic thought from your list"))
        time.sleep(3)
        print(bot.format("How does it sound?💫"))
        automatic_thought = input()
        print(bot.format("Considering it, respond to the following questions"))
        time.sleep(3)
        probing_questions = chatbot_function.get_data('thought_record_probing_questions')
        answers = {}
        for i in range(len(probing_questions)):
            time.sleep(1)
            print(bot.format(probing_questions[i]))
            response = input()
            key = "Response at question " + str(i + 1)
            answers[key] = response

        structured_answers = ''
        for key in answers:
            structured_answers = structured_answers + key + ': ' + answers[key] + '\n'
        print(bot.format("So, for the moment, the list looks like this: " + structured_answers))
        time.sleep(2)
        print(bot.format("Now, " + user_name + ", use your responses to these questions to create an alternative response"))
        time.sleep(2)
        print(bot.format("This answer could be used for defending the automatic thought that may cause your negative emotion"))
        time.sleep(2)
        print(bot.format("When you are ready, please let me know what idea you developed 🥺"))
        final_answer = input()
        final_answer_interpretation, _ = sentiment_analysis.predict_text(final_answer)
        automatic_thought_interpretation, _ = sentiment_analysis.predict_text(automatic_thought)
        change_in_mood = final_answer_interpretation - automatic_thought_interpretation
        if final_answer_interpretation > 0.33 and change_in_mood > 0:
            print(bot.format("Good job, " + user_name + "! 🎉"))
            time.sleep(1)
            print(bot.format("I am more than happy to see that you succeed in reconstructing the way in which you think!"))
            time.sleep(1)
            print(bot.format("Don't forget to apply this exercise every time to feel overwhelmed by a thought."))
            time.sleep(1)
            chatbot_function.goodbye()
        else:
            chatbot_function.recommend_supervised_help()

