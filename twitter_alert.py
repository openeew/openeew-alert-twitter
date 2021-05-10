import tweepy
from os import getenv

consumer_key = getenv("TWITTER_CONSUMER_KEY", "")
consumer_secret = getenv("TWITTER_CONSUMER_SECRET", "")
access_token = getenv("TWITTER_ACCESS_TOKEN", "")
access_token_secret = getenv("TWITTER_TOKEN_SECRET", "")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


def send_tweet(message):
    if api.verify_credentials():
        print("Authentication Ok")
        api.update_status(status=message)
        print("Tweet message sent")
    else:
        print("Authentication failed")
