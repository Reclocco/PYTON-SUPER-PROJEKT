import tweepy

consumer_key = 'a71AzCqamdL5TsPFD3iuLYhWY'
consumer_secret = '832tfVnw9394JP78sA0N3RXZQU2HxXg0aFRIMw3dUjh77LhEqS'
access_token = '1255793475058098178-eyMC4L0jFFweQPVeRJITP1CAEjQLtI'
access_token_secret = 'rLtyctsrzYVEpVZGPQifuuY63hxalLbir6KT04e9IwheW'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
