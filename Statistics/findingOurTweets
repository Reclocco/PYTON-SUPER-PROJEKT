from config import *
import tweepy

api = tweepy.API(auth, wait_on_rate_limit=True)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)


public_tweets = api.home_timeline()

query = "Ty. This is exactly telling red states to rig their virus death figures #trumpownseverydeath trump"
language = "en"
data_since = "2020-05-12"
results = api.search(q=query, lang=language, since = data_since)

for tweet in results:
    print (tweet.user.screen_name,"Tweeted:",tweet.text)
# po query wyszukuje tweety naszego bota dopasowane    
    
