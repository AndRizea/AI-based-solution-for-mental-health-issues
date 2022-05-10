import chatbot_functions as chatbot_function
import sentiment_analysis


def identify_sentiment(text):
    response = text
    prediction, _ = sentiment_analysis.predict_text(response)
    return prediction


def sadness_det_if_feel_better_action(username=None):
    sadness_det_if_feel_better_action = chatbot_function.get_data('determine_if_feel_better_action')
    replies = chatbot_function.get_reply(sadness_det_if_feel_better_action, 3, username)
    return replies


def sadness_describe_feel_better_action(username=None):
    sadness_feel_better_replies = chatbot_function.get_data('handle_sadness')
    replies = chatbot_function.get_reply(sadness_feel_better_replies, 3, username)
    return replies


def sadness_thought_record_intro(username=None):
    thought_recording_intro = chatbot_function.get_data('thought_record_intro')
    replies = chatbot_function.get_reply(thought_recording_intro, 3, username)
    return replies


def sadness_thought_record_details(username=None):
    thought_recording_details = chatbot_function.get_data('thought_record_details')
    replies = chatbot_function.get_reply(thought_recording_details, 3, username)
    return replies


def sadness_thought_record_steps(username=None):
    thought_record_steps = chatbot_function.get_data('thought_record_steps')
    replies = chatbot_function.get_reply(thought_record_steps, 3, username)
    return replies


def sadness_find_automatic_thought(username=None):
    find_automatic_thought = chatbot_function.get_data('find_automatic_thought')
    replies = chatbot_function.get_reply(find_automatic_thought, 3, username)
    return replies


class Chatbot:
    phase = 0
    #bot = "CloudBot ☁: {0}"
    bot = "{0}"
    user = "USER: {0}"
    name = ""

    def __init__(self):
        self.accept_help = 0
        self.phase = 0

    def sadness_explain_reason(self):
        text = ""
        text += self.bot.format(
            self.name + ", I am sorry to hear that... Please, go ahead and tell me more about your feeling")
        return text

    def talk(self, text):
        print("phase= " + str(self.phase))
        reply = ""
        scenario = ""

        if self.phase == 0:
            self.phase = self.phase + 1
            self.name = text
            reply = chatbot_function.greeting(text)
            return reply

        if self.phase == 1:
            prediction = identify_sentiment(text=text)
            self.phase = self.phase + 0.1
            if prediction < 0.67:
                scenario = "ANXIETY & DEPRESSION"
                reply = self.sadness_explain_reason()
                return reply
            else:
                text1 = self.bot.format(
                    "Sorry, but for the moment I can't understand what are you really feeling. I will get better in the following period, I promise!")
                text2 = self.bot.format("Until then, stay strong!")
                return text1, text2

        if self.phase == 1.1:
            self.phase = round(self.phase + 0.1, 2)
            return sadness_describe_feel_better_action(self.name)

        if self.phase == 1.2:
            self.phase = round(self.phase + 0.1, 2)
            return sadness_det_if_feel_better_action(self.name)

        if text.lower() == "yes" and self.phase == 1.3:
            self.phase = round(self.phase + 0.1, 2)
            return self.bot.format(
                "This sounds good!✨ Would you want to tell me more about it? Please respond by YES or NO")
        elif text.lower() == "no" and self.phase == 1.3:
            self.phase = round(self.phase + 0.2, 2)
            reply = sadness_thought_record_intro(self.name)
            return reply

        if text.lower() == "yes" and self.phase == 1.4:
            self.phase = round(self.phase + 0.01, 3)
            return self.bot.format("Go ahead, " + self.name + "!")
        elif text.lower() == "no" and self.phase == 1.4:
            replies = chatbot_function.goodbye(self.name)
            scenario = "GOODBYE"
            return replies

        if self.phase == 1.41:
            self.phase = round(self.phase + 0.01, 3)
            return self.bot.format(
                "Amazing! " + text + " sounds great, " + self.name + ". For the moment, what would you like to add to our conversation?")

        if self.phase == 1.42:
            replies = chatbot_function.goodbye(self.name)
            scenario = "GOODBYE"
            return replies

        if text.lower() == "yes" and self.phase == 1.5:
            self.phase = round(self.phase + 0.01, 3)
        elif text.lower() == "no" and self.phase == 1.5:
            self.phase = round(self.phase + 0.01, 3)
            reply = sadness_thought_record_details(self.name)
            return reply

        if self.phase == 1.51:
            self.phase = round(self.phase + 0.01, 3)
            reply = sadness_thought_record_steps(self.name)
            return reply

        if text.lower() == "ready" and self.phase == 1.52:
            self.phase = round(self.phase + 0.01, 3)
            reply = sadness_find_automatic_thought(self.name)
            return reply

        if self.phase == 1.53:
            probing_questions = chatbot_function.get_data('thought_record_probing_questions')
            answers = {}
            for i in range(len(probing_questions)):
                print(self.phase)
                self.phase = round(1.53 + (i + 1) * 0.001, 4)
                print(i)
                print(self.phase)
                if self.phase == round(1.53 + (i + 1) * 0.001, 4):
                    print(probing_questions[i])
                    return self.bot.format(probing_questions[i])
                    response = text
                    key = "Response at question " + str(i + 1)
                    answers[key] = response

            structured_answers = ''
            for key in answers:
                structured_answers = structured_answers + key + ': ' + answers[key] + '\n'
                print(structured_answers)
                #return self.bot.format(structured_answers)

        if scenario == "GOODBYE":
            exit()
