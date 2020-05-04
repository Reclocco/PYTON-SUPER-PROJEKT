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
    csvFile = open('%s - hasztag.csv' % hashtag, 'a')
    csvWriter = csv.writer(csvFile)

    for tweet in tweepy.Cursor(api.search, hashtag, count=100,
                               lang="pl",
                               since="2017-04-03").items():
        #print(tweet.created_at, tweet.text)
        csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8')])


def getUserTwittsData(user):
    alltweets = []
    new_tweets = api.user_timeline(screen_name=user, count=200)
    alltweets.extend(new_tweets)
    oldest = alltweets[-1].id - 1

    while len(new_tweets) > 0:
        #print("downloading tweets before %s" % (oldest))
        new_tweets = api.user_timeline(screen_name=user, count=200, max_id=oldest)
        alltweets.extend(new_tweets)
        oldest = alltweets[-1].id - 1

        #print("...%s tweets downloaded so far" % (len(alltweets)))

    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]

    with open('%s_tweets.csv' % user, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)
    pass

getTwittsForHashtag("#SYCOW")
getUserTwittsData("polsport")
