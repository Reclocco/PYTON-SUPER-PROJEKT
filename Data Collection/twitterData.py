import tweepy
import csv

consumer_key = 'a71AzCqamdL5TsPFD3iuLYhWY'
consumer_secret = '832tfVnw9394JP78sA0N3RXZQU2HxXg0aFRIMw3dUjh77LhEqS'
access_token = '1255793475058098178-eyMC4L0jFFweQPVeRJITP1CAEjQLtI'
access_token_secret = 'rLtyctsrzYVEpVZGPQifuuY63hxalLbir6KT04e9IwheW'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

def getTwittsForHashtag(hashtag):

    csvFile = open('%s - hasztag.csv' %hashtag, 'a')
    csvWriter = csv.writer(csvFile)

    for tweet in tweepy.Cursor(api.search, hashtag, count=100,
                               lang="pl",
                               since="2017-04-03").items():
        print(tweet.created_at, tweet.text)
        csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])


def getUserTwittsData():
    # TODO napisać funkcję
    pass


getTwittsForHashtag("#SYCOW")
