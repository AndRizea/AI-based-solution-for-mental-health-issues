import chatbot_functions as chatbot_function
import time
import sentiment_analysis

bot = "CloudBot ☁: {0}"
user = "USER: {0}"


def thought_record(user_name):
    thought_record_intro = chatbot_function.get_data('thought_record_intro')
    chatbot_function.get_reply(username=user_name, data=thought_record_intro, time_sleep=3)
    ready = input()
    if ready.lower() == 'ready':
        find_automatic_thought = chatbot_function.get_data('find_automatic_thought')
        chatbot_function.get_reply(username=user_name, data=find_automatic_thought, time_sleep=3)
        automatic_thought = input()
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
        find_alternative_response = chatbot_function.get_data('find_alternative_response')
        chatbot_function.get_reply(username=user_name, data=find_alternative_response, time_sleep=3)
        final_answer = input()
        final_answer_interpretation, _ = sentiment_analysis.predict_text(final_answer)
        automatic_thought_interpretation, _ = sentiment_analysis.predict_text(automatic_thought)
        change_in_mood = final_answer_interpretation - automatic_thought_interpretation
        if final_answer_interpretation > 0.33 and change_in_mood > 0:
            congratulations = chatbot_function.get_data('congratulations')
            chatbot_function.get_reply(username=user_name, data=congratulations, time_sleep=2)
        else:
            chatbot_function.recommend_supervised_help()

