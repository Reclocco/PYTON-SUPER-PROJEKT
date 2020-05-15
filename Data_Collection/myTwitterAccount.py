from Data_Collection.twitterData import api, getUserTweetsData


def getMyTweetsData(number):
    myAccount = api.me()
    id = myAccount._json['screen_name']
    getUserTweetsData(id, number)


def postTweet(text):
    api.update_status(text)


def deleteLastTweet():
    myAccountName = api.me()._json['screen_name']
    lastTweets = api.user_timeline(screen_name=myAccountName, count=1)
    if len(lastTweets) > 0:
        lastId = lastTweets[0]._json['id']
        api.destroy_status(lastId)
        
        
def deleteTweet(number):
    myAccountName = api.me()._json['screen_name']
    tweets = api.user_timeline(screen_name=myAccountName, count=1)
    if len(tweets) > 0:
        id = tweets[number]._json['id']
        api.destroy_status(id)


if __name__ == '__main__':
    # postTweet('Yey, I will be a bot and this is test tweet')
    #deleteTweet(0)
    # getMyTweetsData(100)
    # deleteLastTweet()
    pass
