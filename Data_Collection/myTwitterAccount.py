from Data_Collection.twitterData import api, getUserTweetsData


def getMyTweetsData(number):
    myAccount = api.me()
    id = myAccount._json['screen_name']
    getUserTweetsData(id, number)


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
