import tweepy
import configparser
import time
import pandas as pd
from datetime import datetime, timezone, timedelta


#Reading keys from config file
config = configparser.ConfigParser(interpolation=None)
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']
bearer_token = config['twitter']['bearer_token']

#API Authorization
client = tweepy.Client(
    bearer_token= bearer_token,
    consumer_key= api_key,
    consumer_secret= api_key_secret,
    access_token= access_token,
    access_token_secret =access_token_secret
)


#Getting Mentions of User
name = "None96682725" 
#name = "elonmusk"


#UTC TIME IS 4 HOURS AHEAD 
while True: 
    end = datetime.now(timezone.utc).replace(microsecond=0)
    start = end - timedelta(seconds=15)
    #tweets = client.get_users_mentions(id=user_id,end_time=end, start_time = start, max_results=100)
    #tweets = client.get_users_mentions(id=user_id,max_results=5)
    tweets = client.search_recent_tweets(query=('@'+name), max_results=10, expansions='author_id', tweet_fields='created_at')
    
    #Pandas dataframe
    columns = ['Time', 'User', 'Tweet']
    data = []

    if tweets.data is None:
        print(end.isoformat()+' no tweets')
        break
    else:
        for tweet in tweets.data:
            #
            #getting tweet info
            tweeter = client.get_user(id=tweet.author_id)
            tweeterinfo = tweeter.data
            tweettime = tweet.created_at - timedelta(hours=4)
            tweettime = tweettime.strftime(" %m/%d/%y %H:%M:%S")

            data.append([tweettime, tweeterinfo.name, tweet.text])
            df = pd.DataFrame(data, columns=columns)
            
            #print('@'+tweeterinfo.username+': '+tweeterinfo.name+tweettime+':'+'\n'+tweet.text)
            #print('------------------')
        df.to_csv('tweets.csv',mode='a', index=False, header=False)
        break
        
        