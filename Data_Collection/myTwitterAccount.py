from Data_Collection.twitterData import api, getUserTweetsData
from pandas import DataFrame as dataframe


def getMyTweetsData(number):
    myAccount = api.me()
    id = myAccount._json['screen_name']
    return getUserTweetsData(id, number)

def getMyRetweetsFavourites(number):
    data = getMyTweetsData(number)
    retweets = data[2::4]
    favourites = data[3::4]
    for e in favourites:
        e = int(e)
    for e in retweets:
        e = int(e)
    #print(data)
    sum_f = sum(favourites)
    sum_r = sum(retweets)
    d = {'retweets': [sum_r], 'favourites': [sum_f]}
    df = dataframe(data=d)
    return (['retweets','favourites'],
            [sum_r,sum_f])



def postTweet(text):
    if len(text) > 0:
        api.update_status(text)


def deleteLastTweet():
    myAccountName = api.me()._json['screen_name']
    lastTweets = api.user_timeline(screen_name=myAccountName, count=1)
    if len(lastTweets) > 0:
        lastId = lastTweets[0]._json['id']
        api.destroy_status(lastId)
       

if __name__ == '__main__':
    # postTweet('Yey, I will be a bot and this is test tweet')
    # getMyTweetsData(100)
    # deleteLastTweet()
    pass
