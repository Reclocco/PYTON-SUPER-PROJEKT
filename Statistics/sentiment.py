import tweepy
from datetime import datetime
from textblob import TextBlob
import matplotlib.pyplot as plt
from config import *

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)


def getE1():
    E1 = "Donald Trump"
    return E1


def getE2():
    E2 = 100
    return E2


def getData():
    keyword = getE1()
    number_of_tweets = getE2()

    polarity_list = []
    numbers_list = []
    number = 1

    for tweet in tweepy.Cursor(api.search, keyword, lang="en").items(number_of_tweets):
        try:
            analysis = TextBlob(tweet.text)
            analysis = analysis.sentiment
            polarity = analysis.polarity
            polarity_list.append(polarity)
            numbers_list.append(number)
            number = number + 1

        except tweepy.TweepError as e:
            print(e.reason)

        except StopIteration:
            break

    axes = plt.gca()
    axes.set_ylim([-1, 2])

    plt.scatter(numbers_list, polarity_list)

    averagePolarity = (sum(polarity_list)) / (len(polarity_list))
    averagePolarity = "{0:.0f}%".format(averagePolarity * 100)
    time = datetime.now().strftime("At: %H:%M\nOn: %m-%d-%y")

    plt.text(0, 1.25, "Average Sentiment:  " + str(averagePolarity) + "\n" + time, fontsize=12,
             bbox=dict(facecolor='none', edgecolor='black', boxstyle='square, pad = 1'))

    plt.title("Sentiment of " + keyword + " on Twitter")
    plt.xlabel("Number of Tweets")
    plt.ylabel("Sentiment")
    plt.show()


if __name__ == '__main__':
    getData()
#Sentiment Analysis is the process of ‘computationally’ 
#determining whether a piece of writing is positive, negative 
#or neutral. It’s also known as opinion mining, deriving the opinion or attitude of a speaker.
