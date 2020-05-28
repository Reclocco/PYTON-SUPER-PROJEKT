import os
import platform
from flask import Flask, render_template
from Machine_Learning.readText import areWordsEnglish
from Machine_Learning.NeuralNetwork import createTweet
from Data_Collection.myTwitterAccount import postTweet, getMyTweetsData

app = Flask(__name__)


@app.route('/home')
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate')
def generate():
    # generate tweets to pass
    # tweet = "lorem impsum tralala poka bimboły jak zdać studia tutorial 5 min fast"
    # TODO dodać animacje ładowania, bo na razie po prostu długo sama strona się ładuje (~ 30s)
    tweet = createForTopic('trump')
    postTweet(tweet)
    return render_template('generate.html', tweet=tweet)


def createForTopic(topic):
    # TODO wybrać odpowiedni plik zależnie od wybranego kafelka
    slash = '/' if platform.system() == 'Linux' else '\\'
    filename = os.path.dirname(os.getcwd()) + slash + 'Data_Collection' + slash + topic + '.txt'
    file = open(filename).read()
    englishText = areWordsEnglish(file)
    tweet = createTweet(englishText, 100, topic)
    return tweet


@app.route('/stats')
def stats():
    # generate twitter statistics data to pass
    # data = "UwU t.. twittew-san, hewwo *-*"
    data = getMyTweetsData(100)
    return render_template('stats.html', data=data)


if __name__ == '__main__':
    app.run(threaded=False)
