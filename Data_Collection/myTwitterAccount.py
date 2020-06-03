from Data_Collection.twitterData import api, getUserTweetsData
from pandas import DataFrame as dataframe
import datetime


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

def change_char(s, p, r):
        return s[:p]+r+s[p+1:]

def getMyTodayYesterdayTweets(number):
    todayCount = 0
    yesterdayCount = 0
    data = getMyTweetsData(number)
    dates = data[0::4]
    newdates = []
    for date in dates:
        newdate = date.split(' ')
        year = newdate[5]
        day = newdate[2]
        if(newdate[1] == 'Jan'):
            month = '01'
        elif (newdate[1] == 'Feb'):
            month = '02'
        elif (newdate[1] == 'Mar'):
            month = '03'
        elif (newdate[1] == 'Apr'):
            month = '04'
        elif (newdate[1] == 'May'):
            month = '05'
        elif (newdate[1] == 'Jun'):
            month = '06'
        elif (newdate[1] == 'Jul'):
            month = '07'
        elif (newdate[1] == 'Aug'):
            month = '08'
        elif (newdate[1] == 'Sep'):
            month = '09'
        elif (newdate[1] == 'Oct'):
            month = '10'
        elif (newdate[1] == 'Nov'):
            month = '11'
        elif (newdate[1] == 'Dec'):
            month = '12'
        new_date = year + "-" + month + "-" + day
        newdates.append(new_date)


    today = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    for date in newdates:
        if(date[0:10] == today[0:10]):
            todayCount += 1
        elif(date[0:10] == yesterday[0:10]):
            yesterdayCount += 1
    return (['yesterday', 'today'],
            [yesterdayCount, todayCount])


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
