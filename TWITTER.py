import tweepy as tp
import configparser as cf

config = cf.ConfigParser()
config.read("config.ini")

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']


auth = tp.OAuthHandler(api_key,api_key_secret)
auth.set_access_token(access_token,access_token_secret)

api = tp.API(auth)

pub = api.home_timeline()

columns = ["Timeline","User","tweet"]
data = []
for tweets in pub:
    data.append([tweets.created_at,tweets.user.screen_name,tweets.text])
    
    
import pandas as pd
df = pd.DataFrame(data,columns=columns)
df