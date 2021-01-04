from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
import pandas as pd
import csv

consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

def scrapetweets(username,search_words, date_since, tweetNumber):
    db_tweets = pd.DataFrame(columns = ['username', 'tweetcreatedts', 'text', 'hashtags'])


    tweets = tweepy.Cursor(api.user_timeline, id = username, q=search_words, lang="tr", since=date_since, tweet_mode='extended').items(tweetNumber)
    tweet_list = [tweet for tweet in tweets]

    for tweet in tweet_list:
        username = tweet.user.screen_name
        tweetcreatedts = tweet.created_at
        hashtags = tweet.entities['hashtags']

        try:
            text = tweet.retweeted_status.full_text
        except AttributeError:  # Not a Retweet
            text = tweet.full_text
        
        ith_tweet = [username, tweetcreatedts, text, hashtags]
        db_tweets.loc[len(db_tweets)] = ith_tweet
  
    print('Veri çekme işlemi sonlandı.')
        
    filename = 'output.csv'
    db_tweets.to_csv(filename, index = False)

search_words = "keywords"
date_since = "2017-01-01"
tweetNumber = 5000
username = 'zekiahmetbayar'
scrapetweets(username,search_words, date_since, tweetNumber)