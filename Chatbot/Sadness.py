import chatbot_functions as chatbot_function


# def det_if_feel_better_action(username=None):
#     sadness_det_if_feel_better_action = chatbot_function.get_data('determine_if_feel_better_action')
#     replies = chatbot_function.get_reply(sadness_det_if_feel_better_action, 3, username)
#     return replies
#
#
# def describe_feel_better_action(username=None):
#     sadness_feel_better_replies = chatbot_function.get_data('handle_sadness')
#     replies = chatbot_function.get_reply(sadness_feel_better_replies, 3, username)
#     return replies


def thought_record_intro(username=None):
    thought_recording_intro = chatbot_function.get_data('thought_record_intro')
    replies = chatbot_function.get_reply(thought_recording_intro, 3, username)
    return replies


def thought_record_details(username=None):
    details = chatbot_function.get_data('thought_record_details')
    replies = chatbot_function.get_reply(details, 3, username)
    return replies


def thought_record_steps(username=None):
    steps = chatbot_function.get_data('thought_record_steps')
    replies = chatbot_function.get_reply(steps, 3, username)
    return replies


def find_automatic_thought(username=None):
    automatic_thought = chatbot_function.get_data('find_automatic_thought')
    replies = chatbot_function.get_reply(automatic_thought, 3, username)
    return replies


class Sadness:
    bot = "{0}"
    username = ""
    is_better_action = True
    is_new_to_exercise = True

    def __init__(self, username):
        self.username = username

    def explain_reason(self):
        text = ""
        text += self.bot.format(
            self.username + ", I am sorry to hear that... Please, go ahead and tell me more about your feeling")
        return text

    def describe_feel_better_action(self, username):
        sadness_feel_better_replies = chatbot_function.get_data('handle_sadness')
        replies = chatbot_function.get_reply(sadness_feel_better_replies, 3, username)
        return replies

    def det_if_feel_better_action(self, username):
        sadness_det_if_feel_better_action = chatbot_function.get_data('determine_if_feel_better_action')
        replies = chatbot_function.get_reply(sadness_det_if_feel_better_action, 3, username)
        return replies

    def thought_record_intro(self, username):
        thought_recording_intro = chatbot_function.get_data('thought_record_intro')
        replies = chatbot_function.get_reply(thought_recording_intro, 3, username)
        return replies

    def thought_record_steps(self, username):
        steps = chatbot_function.get_data('thought_record_steps')
        replies = chatbot_function.get_reply(steps, 3, username)
        return replies

    def thought_record_details(self, username):
        details = chatbot_function.get_data('thought_record_details')
        replies = chatbot_function.get_reply(details, 3, username)
        return replies

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
                return chatbot_function.goodbye(username)
        else:
            return self.thought_record_intro(username)

    def add_to_conversation(self, username):
        return self.bot.format("Amazing, " + username + "!. For the moment, what would you like to add to our conversation?")

    def new_to_exercise(self, username, user_input):
        if user_input.lower() == "no":
            reply = self.thought_record_details(username)
        elif user_input.lower() == "yes":
            self.is_new_to_exercise = False
            reply = self.thought_record_steps(username)
        return reply

    def user_ready(self, user_input):
        if user_input.lower == "ready":
            find_thought = find_automatic_thought(self.username)
            return find_thought
