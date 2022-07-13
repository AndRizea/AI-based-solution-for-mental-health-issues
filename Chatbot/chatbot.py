import chatbot_functions as chatbot_function
import sentiment_analysis
from Scenario import Scenario
from datetime import datetime
import json
import report
import os


def identify_sentiment(text):
    response = text
    prediction, _ = sentiment_analysis.predict_text(response)
    return prediction


def export_conv_history(dictionary):
    with open("static/conversation_history.json", 'w') as outfile:
        json.dump(dictionary, outfile)


class Chatbot(Scenario):
    bot = "{0}"
    user = "USER: {0}"

    def __init__(self, username):
        super().__init__(username)
        self.questions_left = 0
        self.name = username
        self.phase = 0
        self.conversation_history = {}
        export_conv_history(self.conversation_history)
        self.reply = ""
        self.is_image = True

        if self.is_image and os.path.exists('static/images/report.png'):
            os.remove("static/images/report.png")
            self.is_image = False

    def explain_reason_sadness(self):
        text = ""
        text += self.bot.format(
            self.name + ", I am sorry to hear that... Please, go ahead and tell me more about your feeling")
        return text

    def talk(self, text):
        print("phase= " + str(self.phase))

        if self.phase == 0:
            start_time = datetime.now()
            self.conversation_history['start_time'] = start_time.strftime("%d %B, %Y, %H:%M:%S")
            self.phase = self.phase + 1
            self.name = text.capitalize()
            self.conversation_history['username'] = self.name
            self.reply = chatbot_function.greeting(self.name)

            return self.reply

        self.conversation_history[self.reply] = text
        print(self.conversation_history)
        scenario = Scenario(self.name)
        sadness = scenario.sadness
        joy = scenario.joy
        self.questions_left = len(sadness.probing_questions)
        prediction = identify_sentiment(text=text)
        print(prediction)

        if self.phase == 1:
            if prediction < 0.67:
                # scenario = "ANXIETY & DEPRESSION"
                self.phase = self.phase + 1
            elif 0.67 <= prediction < 0.8:
                self.phase = self.phase + 2
            else:
                self.phase = self.phase + 3

        if self.phase == 2:
            self.phase = round(self.phase + 0.1, 2)
            self.reply = sadness.explain_reason_sadness()
            return sadness.explain_reason_sadness()

        if self.phase == 3:
            self.phase = round(self.phase + 0.1, 2)
            self.reply = sadness.explain_reason_anger()
            return self.reply

        self.conversation_history[self.reply] = text

        if self.phase == 2.1:
            self.phase = round(self.phase + 0.1, 2)
            self.reply = sadness.describe_feel_better_action(self.name)
            return sadness.describe_feel_better_action(self.name)

        if self.phase == 3.1:
            self.phase = 2.2
            self.reply = sadness.handle_anger(self.name)
            return self.reply

        self.conversation_history[self.reply] = text

        if self.phase == 2.2:
            if sadness.is_better_action:
                self.phase = round(self.phase + 0.1, 2)
            else:
                self.phase = round(self.phase + 0.2, 2)
            self.reply = sadness.det_if_feel_better_action(self.name)
            return sadness.det_if_feel_better_action(self.name)

        self.conversation_history[self.reply] = text

        if self.phase == 2.3:
            if text.lower() == "no":
                self.phase = 2.4
            else:
                self.phase = round(self.phase + 0.01, 3)
            self.reply = sadness.better_action(text, self.name)
            return sadness.better_action(text, self.name)

        self.conversation_history[self.reply] = text

        if self.phase == 2.31:
            self.phase = round(self.phase + 0.01, 3)
            self.reply = sadness.handle_better_action(self.name, sadness.is_better_action, text)
            if not sadness.continue_conversation:
                end_time = datetime.now()
                self.conversation_history['end_time'] = end_time.strftime("%d %B, %Y, %H:%M:%S")
                export_conv_history(self.conversation_history)
                report.generate_graph_report('static/conversation_history.json')
            return sadness.handle_better_action(self.name, sadness.is_better_action, text)

        self.conversation_history[self.reply] = text

        if self.phase == 2.32:
            self.phase = round(self.phase + 0.01, 3)
            self.reply = sadness.add_to_conversation(self.name)
            return sadness.add_to_conversation(self.name)

        self.conversation_history[self.reply] = text

        if self.phase == 2.33:
            self.reply = chatbot_function.goodbye(self.name)
            end_time = datetime.now()
            self.conversation_history['end_time'] = end_time.strftime("%d %B, %Y, %H:%M:%S")
            export_conv_history(self.conversation_history)
            report.generate_graph_report('static/conversation_history.json')
            return chatbot_function.goodbye(self.name)

        self.conversation_history[self.reply] = text

        if self.phase == 2.4:
            self.phase = round(self.phase + 0.01, 3)
            self.reply = sadness.new_to_exercise(self.name, text)
            return sadness.new_to_exercise(self.name, text)

        self.conversation_history[self.reply] = text

        if self.phase == 2.41:
            self.phase = round(self.phase + 0.01, 3)
            self.reply = sadness.exercise_steps(self.name)
            return self.reply

        self.conversation_history[self.reply] = text

        if self.phase == 2.42:
            self.phase = round(self.phase + 0.01, 3)
            self.reply = sadness.user_ready(self.name, text)
            return self.reply

        self.conversation_history[self.reply] = text

        if self.phase == 2.43 and self.questions_left > 0:
            print(self.questions_left)
            self.phase = round(self.phase + 0.01, 3)
            self.reply = sadness.get_question(len(sadness.probing_questions) - self.questions_left)
            # self.questions_left = self.questions_left - 1
            return self.reply

        self.questions_left = self.questions_left - 1
        print(self.questions_left)
        self.conversation_history[self.reply] = text

        if self.phase == 2.44 and self.questions_left > 0:
            print(self.questions_left)
            self.phase = round(self.phase + 0.01, 3)
            self.reply = sadness.get_question(len(sadness.probing_questions) - self.questions_left)
            # self.questions_left = self.questions_left - 1
            return self.reply

        self.conversation_history[self.reply] = text
        self.questions_left = self.questions_left - 1

        if self.phase == 2.45 and self.questions_left > 0:
            self.phase = round(self.phase + 0.01, 3)
            self.reply = sadness.get_question(2)
            # self.questions_left = self.questions_left - 1
            return self.reply

        self.conversation_history[self.reply] = text
        self.questions_left = self.questions_left - 1

        if self.phase == 2.46:
            self.phase = round(self.phase + 0.01, 3)
            self.reply = sadness.get_question(3)
            # self.questions_left = self.questions_left - 1
            return self.reply

        self.conversation_history[self.reply] = text
        self.questions_left = self.questions_left - 1

        if self.phase == 2.47 and self.questions_left > 0:
            self.phase = round(self.phase + 0.01, 3)
            self.reply = sadness.get_question(len(sadness.probing_questions) - self.questions_left)
            # self.questions_left = self.questions_left - 1
            return self.reply

        self.conversation_history[self.reply] = text
        self.questions_left = self.questions_left - 1

        if self.phase == 2.48 and self.questions_left > 0:
            self.phase = round(self.phase + 0.01, 3)
            self.reply = sadness.get_question(len(sadness.probing_questions) - self.questions_left)
            # self.questions_left = self.questions_left - 1
            return self.reply

        self.conversation_history[self.reply] = text
        self.questions_left = self.questions_left - 1

        if self.phase == 2.49 and self.questions_left > 0:
            self.phase = round(self.phase + 0.01, 3)
            self.reply = sadness.get_question(len(sadness.probing_questions) - self.questions_left)
            # self.questions_left = self.questions_left - 1
            return self.reply

        self.conversation_history[self.reply] = text
        self.questions_left = self.questions_left - 1

        if self.phase == 2.50 and self.questions_left > 0:
            self.phase = round(self.phase + 0.01, 3)
            self.reply = sadness.get_question(len(sadness.probing_questions) - self.questions_left)
            # self.questions_left = self.questions_left - 1
            return self.reply

        self.conversation_history[self.reply] = text
        self.questions_left = self.questions_left - 1

        if self.phase == 2.51 and self.questions_left > 0:
            self.phase = round(self.phase + 0.01, 3)
            self.reply = sadness.get_question(len(sadness.probing_questions) - self.questions_left)
            # self.questions_left = self.questions_left - 1
            return self.reply

        self.conversation_history[self.reply] = text

        if self.phase == 2.52:
            self.phase = round(self.phase + 0.01, 3)
            self.reply = sadness.alternative_thought(self.name)
            return self.reply

        self.conversation_history[self.reply] = text
        alternative_thought = text

        if self.phase == 2.53:
            scenario = "END"
            final_prediction = identify_sentiment(alternative_thought)
            if 0.7 >= final_prediction:
                self.reply = sadness.recommend_supervised_help(self.name)
            else:
                self.reply = sadness.congratulations(self.name)
            end_time = datetime.now()
            self.conversation_history['end_time'] = end_time.strftime("%d %B, %Y, %H:%M:%S")
            export_conv_history(self.conversation_history)
            report.generate_graph_report('static/conversation_history.json')
            return self.reply

        if self.phase == 4:
            self.phase = round(self.phase + 0.1, 2)
            self.reply = joy.handle_joy(self.name)
            return self.reply

        self.conversation_history[self.reply] = text

        if self.phase == 4.1:
            self.phase = round(self.phase + 0.1, 2)
            self.reply = joy.recommend_podcast(self.name)
            return self.reply

        self.conversation_history[self.reply] = text

        if self.phase == 4.2:
            if text.lower() == "yes":
                self.phase = round(self.phase + 0.1, 2)
                self.reply = joy.list_podcast(self.name)
                return self.reply
            else:
                self.reply = chatbot_function.goodbye(self.name)
                end_time = datetime.now()
                self.conversation_history['end_time'] = end_time.strftime("%d %B, %Y, %H:%M:%S")
                export_conv_history(self.conversation_history)
                report.generate_graph_report('static/conversation_history.json')
                return chatbot_function.goodbye(self.name)

        if self.phase == 4.3:
            self.reply = chatbot_function.goodbye(self.name)
            end_time = datetime.now()
            self.conversation_history['end_time'] = end_time.strftime("%d %B, %Y, %H:%M:%S")
            export_conv_history(self.conversation_history)
            report.generate_graph_report('static/conversation_history.json')
            self.phase = 0
            return chatbot_function.goodbye(self.name)
