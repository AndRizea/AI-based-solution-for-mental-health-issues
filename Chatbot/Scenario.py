import chatbot_functions as chatbot_function
import sentiment_analysis



def identify_sentiment(text):
    response = text
    prediction, _ = sentiment_analysis.predict_text(response)
    return prediction


class Scenario:
    bot = "{0}"

    # username = ""

    def __init__(self, username):
        self.username = username
        self.sadness = self.Sadness(self.username)
        self.joy = self.Joy(self.username)

    class Sadness:
        bot = "{0}"
        is_better_action = True
        is_new_to_exercise = True
        continue_conversation = True

        def __init__(self, username):
            self.username = username
            self.probing_questions = chatbot_function.get_probing_questions()
            self.questionNo = 0

        def explain_reason_sadness(self):
            text = ""
            text += self.bot.format(
                self.username + ", I am sorry to hear that... Please, go ahead and tell me more about your feeling")
            return text, self.describe_feel_better_action

        def describe_feel_better_action(self, username, user_input):
            sadness_feel_better_replies = chatbot_function.get_data('handle_sadness')
            replies = chatbot_function.get_reply(sadness_feel_better_replies, username)
            return replies, self.det_if_feel_better_action

        def det_if_feel_better_action(self, username, user_input):
            sadness_det_if_feel_better_action = chatbot_function.get_data('determine_if_feel_better_action')
            replies = chatbot_function.get_reply(sadness_det_if_feel_better_action, username)
            return replies, self.better_action

        def better_action(self, username, user_input):
            if user_input.lower() == "yes":
                return self.bot.format(
                    "This sounds good!✨ Would you want to tell me more about it? Please respond by YES or NO"), \
                       self.handle_better_action
            elif user_input.lower() == "no":
                self.is_better_action = False
                return self.thought_record_intro(username), self.new_to_exercise

        def thought_record_intro(self, username):
            thought_recording_intro_reply = chatbot_function.get_data('thought_record_intro')
            replies = chatbot_function.get_reply(thought_recording_intro_reply, username)
            return replies

        def new_to_exercise(self, username, user_input):
            if user_input.lower() == "no":
                reply = self.thought_record_details(username, "")
                return reply, self.thought_record_steps
            elif user_input.lower() == "yes":
                self.is_new_to_exercise = False
                reply = self.start_exercise_directly(username, "")
                return reply, self.thought_record_steps

        def thought_record_details(self, username, user_input):
            details = chatbot_function.get_data('thought_record_details')
            replies = chatbot_function.get_reply(details, username)
            return replies

        def start_exercise_directly(self, username, user_input):
            data = chatbot_function.get_data('thought_record_knew_exercise')
            reply = chatbot_function.get_reply(data, username)
            return reply

        def thought_record_steps(self, username, user_input):
            steps = chatbot_function.get_data('thought_record_steps')
            replies = chatbot_function.get_reply(steps, username)
            return replies, self.user_ready

        def user_ready(self, username, user_input):
            if user_input.lower() == "ready" or user_input.lower() == "rady" or user_input.lower() == "redy" or user_input.lower() == "rdy" or user_input.lower() == "yes":
                find_thought = self.find_automatic_thought(username)
                return find_thought, self.questions

        def find_automatic_thought(self, username):
            automatic_thought = chatbot_function.get_data('find_automatic_thought')
            replies = chatbot_function.get_reply(automatic_thought, username)
            return replies

        def questions(self, username, user_input):
            reply = self.get_question(self.questionNo)
            if self.questionNo < 8:
                self.questionNo += 1
                return reply, self.questions
            else:
                return reply, self.find_alternative_thought

        def find_alternative_thought(self, username, user_input):
            data = chatbot_function.get_data('find_alternative_response')
            reply = chatbot_function.get_reply(data, username)
            return reply, self.end_exercise

        def end_exercise(self, username, user_input):
            if identify_sentiment(user_input) > 0.7:
                reply, _ = self.congratulations(username, user_input)
                return reply, None
            else:
                reply, _ = self.recommend_supervised_help(username, user_input)
                return reply, None

        def recommend_supervised_help(self, username, user_input):
            data = chatbot_function.get_data('recommend_supervised_help')
            reply = chatbot_function.get_reply(data, username)
            return reply, chatbot_function.goodbye

        def congratulations(self, username, user_input):
            data = chatbot_function.get_data('congratulations')
            reply = chatbot_function.get_reply(data, username)
            return reply, chatbot_function.goodbye

        def handle_better_action(self, username, user_input):
            if user_input.lower() == "yes":
                return self.bot.format("Go ahead, " + username + "!"), self.add_to_conversation
            else:
                self.continue_conversation = False
                return chatbot_function.goodbye(username)

        def add_to_conversation(self, username, user_input):
            return self.bot.format(
                "Amazing, " + username + "!. For the moment, what would you like to add to our conversation?"), chatbot_function.goodbye

        def exercise_steps(self, username):
            # if self.is_new_to_exercise:
            return self.thought_record_steps(username)

        def get_question(self, index):
            return self.probing_questions[index]

        def alternative_thought(self, username):
            return self.find_alternative_thought(username)

        def explain_reason_anger(self):
            text = ""
            text += self.bot.format(
                self.username + ", I see the problem and I am here for you. Please, go ahead and tell me more about your feeling")
            return text, self.handle_anger

        def handle_anger(self, username, user_input):
            data = chatbot_function.get_data('handle_anger')
            reply = chatbot_function.get_reply(data, username)
            return reply, self.det_if_feel_better_action

    class Joy:
        bot = "{0}"
        is_interested_podcast = True

        def __init__(self, username):
            self.username = username

        def handle_joy(self, username):
            data = chatbot_function.get_data('handle_joy')
            replies = chatbot_function.get_reply(data, username)
            return replies, self.recommend_podcast

        def recommend_podcast(self, username, user_input):
            data = chatbot_function.get_data('recommend_podcast')
            replies = chatbot_function.get_reply(data, username)
            return replies, self.list_podcast

        def list_podcast(self, username, user_input):
            if user_input.lower() == "yes":
                data = chatbot_function.get_data('podcast_suggestion')
                replies = chatbot_function.get_reply(data, username)
                return replies, chatbot_function.goodbye
            else:
                return chatbot_function.goodbye(username)
