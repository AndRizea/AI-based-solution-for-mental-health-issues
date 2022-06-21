import chatbot_functions as chatbot_function
import sentiment_analysis
from Sadness import Sadness


def identify_sentiment(text):
    response = text
    prediction, _ = sentiment_analysis.predict_text(response)
    return prediction


class Chatbot(Sadness):
    phase = 0
    # bot = "CloudBot ☁: {0}"
    bot = "{0}"
    user = "USER: {0}"

    def __init__(self, username):
        super().__init__(username)
        self.name = username
        self.phase = 0

    def explain_reason(self):
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
            self.name = text.capitalize()

            reply = chatbot_function.greeting(self.name)
            return reply

        sadness = Sadness(self.name)
        prediction = identify_sentiment(text=text)

        if self.phase == 1:
            if prediction < 0.67:
                scenario = "ANXIETY & DEPRESSION"
                self.phase = self.phase + 1
            else:
                text1 = self.bot.format(
                    "Sorry, but for the moment I can't understand what are you really feeling. I will get better in the following period, I promise!")
                text2 = self.bot.format("Until then, stay strong!")
                return text1, text2

        if self.phase == 2:
            self.phase = round(self.phase + 0.1, 2)
            return sadness.explain_reason()

        if self.phase == 2.1:
            self.phase = round(self.phase + 0.1, 2)
            return sadness.describe_feel_better_action(self.name)

        if self.phase == 2.2:
            if sadness.is_better_action:
                self.phase = round(self.phase + 0.1, 2)
            else:
                self.phase = round(self.phase + 0.2, 2)
            return sadness.det_if_feel_better_action(self.name)

        if self.phase == 2.3:
            if text.lower() == "no":
                self.phase = 2.4
            else:
                self.phase = round(self.phase + 0.01, 3)
            return sadness.better_action(text, self.name)

        if self.phase == 2.31:
            self.phase = round(self.phase + 0.01, 3)
            return sadness.handle_better_action(self.name, sadness.is_better_action, text)

        if self.phase == 2.32:
            self.phase = round(self.phase + 0.01, 3)
            return sadness.add_to_conversation(self.name)

        if self.phase == 2.33:
            return chatbot_function.goodbye(self.name)

        if self.phase == 2.4:
            self.phase = round(self.phase + 0.01, 3)
            return sadness.new_to_exercise(self.name, text)

        if self.phase == 2.41:
            return self.bot.format("questions now because user ready")
