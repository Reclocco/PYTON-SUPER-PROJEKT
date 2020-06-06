from Data_Collection.twitterData import api
from config import *


def get_followers(person):
    count = 0

    influencer = api.get_user(screen_name=person)
    number_of_followers = influencer.followers_count
    print("number of followers count : ", number_of_followers)
    return count


user = api.me()._json['screen_name']
get_followers(user)
