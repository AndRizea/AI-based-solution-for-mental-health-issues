from flask import Flask, render_template, request, jsonify
import time
import Chatbot
from Sadness import Sadness

app = Flask(__name__)
chatbot = Chatbot.Chatbot(Sadness)


@app.get("/")
def index_get():
    return render_template("base.html")


@app.get("/team")
def index_get_team():
    return render_template("team.html")


@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # text=""
    # text += temp
    # while temp!="":
    #     temp = request.get_json().get("message")
    #     text += temp
    # TODO: check if text is valid
    response = chatbot.talk(text)
    message = {"answer": response}
    time.sleep(0.5)
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)
