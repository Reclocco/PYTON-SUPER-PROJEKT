import tweepy
import csv

consumer_key = 'a71AzCqamdL5TsPFD3iuLYhWY'
consumer_secret = '832tfVnw9394JP78sA0N3RXZQU2HxXg0aFRIMw3dUjh77LhEqS'
access_token = '1255793475058098178-eyMC4L0jFFweQPVeRJITP1CAEjQLtI'
access_token_secret = 'rLtyctsrzYVEpVZGPQifuuY63hxalLbir6KT04e9IwheW'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)


def getTweetsForHashtag(hashtag, number):
    fullText = ''
    for tweet in tweepy.Cursor(api.search, hashtag,
                               lang="en",
                               # since="2017-04-03",
                               tweet_mode='extended'
                               ).items(number):
        # every tweet in new line
        fullText += formatText(tweet._json) + '\n'
    with open('%s - hasztag.txt' % hashtag, 'w+') as f:
        f.write(fullText)


def getUserTweetsData(user, number):
    all_tweets = api.user_timeline(screen_name=user,
                                   count=number,
                                   tweet_mode='extended')
    with open('%s_tweets.csv' % user, 'w+') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text", "retweets", "likes"])
        for tweet in all_tweets:
            jsonTweet = tweet._json
            row = [jsonTweet['id'],
                   jsonTweet['created_at'],
                   formatText(jsonTweet),
                   jsonTweet['retweet_count'],
                   jsonTweet['favorite_count']]
            writer.writerow(row)


def formatText(jsonTweet):
    text = str(jsonTweet['full_text'])
    # # remove hashtags
    # for h in jsonTweet['entities']['hashtags']:
    #     hashtag = h['text']
    #     # text = text.replace(hashtag, '')
    # # remove mentions
    # for u in jsonTweet['entities']['user_mentions']:
    #     user = u['screen_name']
    #     text = text.replace(user, '')
    # remove links
    while 'http' in text:
        start = text.index('http')
        try:
            end = text.index(' ', start)
        except ValueError:
            end = len(text)
        text = text[:start - 1] + text[end:]
    # possible 94 characters from ASCII table
    text = ''.join(e for e in text if 31 < ord(e) < 126)
    # remove RT
    text = text.replace('RT', '')
    # remove trailing spaces
    text = ' '.join(text.split())
    return text


def csvToText(cfile, tfile):
    csv_file = cfile
    txt_file = tfile
    with open(txt_file, "w") as my_output_file:
        with open(csv_file, "r") as my_input_file:
            [my_output_file.write(" ".join(row) + '\n') for row in csv.reader(my_input_file)]
        my_output_file.close()


if __name__ == '__main__':
    getTweetsForHashtag("relax", 100)
    getUserTweetsData("polsport", 200)
