import matplotlib.pyplot as plot
from matplotlib.pyplot import figure
import sentiment_analysis
import json

plot.clf()
plot.cla()
plot.close()


def generate_graph_report(filename):
    with open(filename) as json_file:
        initial_data = json.load(json_file)

    del initial_data['start_time']
    del initial_data['username']
    del initial_data['end_time']
    user_answers = list(initial_data.values())
    print(user_answers)

    dictionary = {}
    for i in range(len(user_answers)):
        #key = user_answers[i]
        key = "ans_" + str(i)
        sentiment_level, _ = sentiment_analysis.predict_text(user_answers[i])
        dictionary[key] = sentiment_level

    print(dictionary)

    xAxis = [key for key, value in dictionary.items()]
    yAxis = [value for key, value in dictionary.items()]
    plot.grid(True)

    ## LINE GRAPH ##
    plot.plot(xAxis, yAxis, color='#4DBEEE', marker='p')
    plot.xlabel('Answers')
    plot.ylabel('Sentiment prediction')
    plot.xticks(xAxis, rotation='vertical')
    plot.savefig('static/images/report.png', dpi=130)
    plot.show()

