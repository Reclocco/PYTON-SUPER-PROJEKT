import tweepy
import datetime


def getTwittsForHashtag(hashtag):
    # TODO założyć konto deweloperskie, zdobyć dane autoryzacyjne
    # how to get conf data:
    # https://towardsdatascience.com/how-to-access-twitters-api-using-tweepy-5a13a206683b
    conf = {
        'consumer_key': None,
        'consumer_secret': None,
        'access_key': None,
        'access_secret': None
    }

    auth = tweepy.OAuthHandler(conf['consumer_key'], conf['consumer_secret'])
    auth.set_access_token(conf['access_key'], conf['access_secret'])
    api = tweepy.API(auth)

    if hashtag[0] == '#':
        hashtag = hashtag[1:]

    # results = []
    # for tweet in tweepy.Cursor(api.search, q='%23' + hashtag).items(1000):
    #     results.append(tweet)

    filename = 'twittsFor#' + hashtag + datetime.datetime.now().strftime("-%d-%m-%y-%H:%M:%S")

    with open(filename, 'w+') as f:
        f.write(' '.join(results))

    return filename


def getMyTwittsData():
    # TODO napisać funkcję
    pass
