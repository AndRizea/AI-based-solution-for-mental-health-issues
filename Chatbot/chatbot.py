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
        self.next_step = None

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
            self.reply, self.next_step = sadness.explain_reason_sadness()
            return self.reply

        if self.phase == 3:
            self.phase = round(self.phase + 0.1, 2)
            self.reply, self.next_step = sadness.explain_reason_anger()
            return self.reply

        if self.phase == 4:
            self.phase = round(self.phase + 0.1, 2)
            self.reply, self.next_step = joy.handle_joy(self.name)
            return self.reply

        self.conversation_history[self.reply] = text

        self.reply, self.next_step = self.next_step(self.name, text)

        if self.next_step is None:
            end_time = datetime.now()
            self.conversation_history['end_time'] = end_time.strftime("%d %B, %Y, %H:%M:%S")
            export_conv_history(self.conversation_history)
            report.generate_graph_report('static/conversation_history.json')

        return self.reply

