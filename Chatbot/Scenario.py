import chatbot_functions as chatbot_function


def thought_record_intro(username=None):
    thought_recording_intro = chatbot_function.get_data('thought_record_intro')
    replies = chatbot_function.get_reply(thought_recording_intro, username)
    return replies


def find_automatic_thought(username=None):
    automatic_thought = chatbot_function.get_data('find_automatic_thought')
    replies = chatbot_function.get_reply(automatic_thought, username)
    return replies


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

        def explain_reason_sadness(self):
            text = ""
            text += self.bot.format(
                self.username + ", I am sorry to hear that... Please, go ahead and tell me more about your feeling")
            return text

        def explain_reason_anger(self):
            text = ""
            text += self.bot.format(
                self.username + ", I see the problem and I am here for you. Please, go ahead and tell me more about your feeling")
            return text

        def describe_feel_better_action(self, username):
            sadness_feel_better_replies = chatbot_function.get_data('handle_sadness')
            replies = chatbot_function.get_reply(sadness_feel_better_replies, username)
            return replies

        def det_if_feel_better_action(self, username):
            sadness_det_if_feel_better_action = chatbot_function.get_data('determine_if_feel_better_action')
            replies = chatbot_function.get_reply(sadness_det_if_feel_better_action, username)
            return replies

        def thought_record_intro(self, username):
            thought_recording_intro = chatbot_function.get_data('thought_record_intro')
            replies = chatbot_function.get_reply(thought_recording_intro, username)
            return replies

        def thought_record_steps(self, username):
            steps = chatbot_function.get_data('thought_record_steps')
            replies = chatbot_function.get_reply(steps, username)
            return replies

        def thought_record_details(self, username):
            details = chatbot_function.get_data('thought_record_details')
            replies = chatbot_function.get_reply(details, username)
            return replies

        def start_exercise_directly(self, username):
            data = chatbot_function.get_data('thought_record_knew_exercise')
            reply = chatbot_function.get_reply(data, username)
            return reply

        def find_alternative_thought(self, username):
            data = chatbot_function.get_data('find_alternative_response')
            reply = chatbot_function.get_reply(data, username)
            return reply

        def recommend_supervised_help(self, username):
            data = chatbot_function.get_data('recommend_supervised_help')
            reply = chatbot_function.get_reply(data, username)
            return reply

        def congratulations(self, username):
            data = chatbot_function.get_data('congratulations')
            reply = chatbot_function.get_reply(data, username)
            return reply

        def handle_anger(self, username):
            data = chatbot_function.get_data('handle_anger')
            reply = chatbot_function.get_reply(data, username)
            return reply

        def better_action(self, user_input, username):
            if user_input.lower() == "yes":
                return self.bot.format(
                    "This sounds good!✨ Would you want to tell me more about it? Please respond by YES or NO")
            elif user_input.lower() == "no":
                self.is_better_action = False
                return thought_record_intro(username)

        def handle_better_action(self, username, is_better_action, user_input):
            if is_better_action:
                if user_input.lower() == "yes":
                    return self.bot.format("Go ahead, " + username + "!")
                else:
                    self.continue_conversation = False
                    return chatbot_function.goodbye(username)
            else:
                return self.thought_record_intro(username)

        def add_to_conversation(self, username):
            return self.bot.format(
                "Amazing, " + username + "!. For the moment, what would you like to add to our conversation?")

        def new_to_exercise(self, username, user_input):
            if user_input.lower() == "no":
                reply = self.thought_record_details(username)
            elif user_input.lower() == "yes":
                self.is_new_to_exercise = False
                reply = self.start_exercise_directly(username)
            return reply

        def exercise_steps(self, username):
            # if self.is_new_to_exercise:
            return self.thought_record_steps(username)

        def user_ready(self, username, user_input):
            if user_input.lower() == "ready":
                find_thought = find_automatic_thought(username)
                return find_thought

        def get_question(self, index):
            return self.probing_questions[index]

        def alternative_thought(self, username):
            return self.find_alternative_thought(username)

    class Joy:
        bot = "{0}"
        is_interested_podcast = True

        def __init__(self, username):
            self.username = username

        def recommend_podcast(self, username):
            data = chatbot_function.get_data('recommend_podcast')
            replies = chatbot_function.get_reply(data, username)
            return replies

        def list_podcast(self, username):
            data = chatbot_function.get_data('podcast_suggestion')
            replies = chatbot_function.get_reply(data, username)
            return replies

        def handle_joy(self, username):
            data = chatbot_function.get_data('handle_joy')
            replies = chatbot_function.get_reply(data, username)
            return replies

        def suggest_podcast(self, user_input, username):
            if user_input.lower() == "NO":
                self.is_interested_podcast = False
