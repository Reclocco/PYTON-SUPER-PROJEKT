import os
import platform
import random
from flask import Flask, render_template
from Machine_Learning.readText import areWordsEnglish
from Machine_Learning.NeuralNetwork import createTweet
from Data_Collection.myTwitterAccount import postTweet, getMyTweetsData, getMyRetweetsFavourites, getMyTodayYesterdayTweets
from Statistics.sentiment import getData

app = Flask(__name__)


@app.route('/home')
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/generate')
def generate():
    # loading
    return render_template('generate.html', tweet='')


@app.route('/generated')
def generated():
    # generate tweets to pass
    # tweet = "lorem impsum tralala poka jak zdać studia tutorial 5 min fast"
    tweet = createForTopic('trump')
    postTweet(tweet)
    return render_template('generated.html', tweet=tweet)


def createForTopic(topic):
    # TODO wybrać odpowiedni plik zależnie od wybranego kafelka
    slash = '/' if platform.system() == 'Linux' else '\\'
    if platform.system() == 'Linux':
        os.chdir('../')
        filename = 'Data_Collection' + slash + topic + '.txt'
    else:
        filename = 'Data_Collection' + slash + topic + '.txt'
    #filename = os.getcwd() + '/Data_Collection' + slash + topic + '.txt'
    file = open(filename).read()
    englishText = areWordsEnglish(file)
    tweet = createTweet(englishText, 100, topic)
    return tweet


@app.route('/stats')
def stats():
    # generate twitter statistics data to pass
    # data = "UwU t.. twittew-san, hewwo *-*"
    data = getMyTweetsData(100)
    names = []
    counts = []
    colors = []
    colors2 = []
    dates = []
    tweetsByDate = []
    keyword = []
    sentiment = []

    names, counts = getMyRetweetsFavourites(100)
    colors = [randomColor() for i in range(2)]
    colors2 = [randomColor() for i in range(2)]
    dates, tweetsByDate = getMyTodayYesterdayTweets(100)
    keyword, sentiment = getData()


    return render_template('stats.html', data=data,max=17000,keyword=keyword,sentiment=sentiment,set=zip(counts,names,colors),set2=zip(tweetsByDate,dates,colors2))

def randomColor():
    return ('#' + str(''.join([random.choice('0123456789ABCDEF') for x in range(6)])))


if __name__ == '__main__':
    app.run(threaded=False)
