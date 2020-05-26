import os
from flask import Flask, render_template
from Machine_Learning.readText import areWordsEnglish
from Machine_Learning.NeuralNetwork import createTweet
from Data_Collection.myTwitterAccount import postTweet

app = Flask(__name__)


@app.route('/home')
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate')
def generate():
    # generate tweets to pass
    # tweet = "lorem impsum tralala poka bimboły jak zdać studia tutorial 5 min fast"
    tweet = createForTopic('trump')
    postTweet(tweet)
    return render_template('generate.html', tweet=tweet)


def createForTopic(topic):
    # TODO wybrać odpowiedni plik zależnie od wybranego kafelka
    filename = os.path.dirname(os.getcwd()) + '/Data_Collection/' + topic + '.txt'
    file = open(filename).read()
    englishText = areWordsEnglish(file)
    tweet = createTweet(englishText, 100, topic)
    return tweet


@app.route('/stats')
def stats():
    # generate twitter statistics data to pass
    data = "UwU t.. twittew-san, hewwo *-*"
    return render_template('stats.html', data=data)


if __name__ == '__main__':
    app.run(threaded=False)
