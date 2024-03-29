from flask import Flask, render_template, request, jsonify
import time
import Chatbot
from Scenario import Scenario


app = Flask(__name__)
chatbot = Chatbot.Chatbot(Scenario)


@app.get("/")
def index_get():
    return render_template("base.html")


@app.get("/team")
def index_get_team():
    return render_template("team.html")


@app.get("/report")
def index_get_report():
    return render_template("report.html")


@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response = chatbot.talk(text)
    message = {"answer": response}
    #time.sleep(0.5)
    return jsonify(message)


if __name__ == "__main__":
    app.run(debug=True)
