# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 20:43:59 2020

@author: broch
"""

import tweepy
import time
import datetime

import credentials as c
from save import Result

auth = tweepy.OAuthHandler(c.CONSUMER_KEY, c.CONSUMER_SECRET)
auth.set_access_token(c.ACCESS_TOKEN, c.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify =True)

results = Result()
# user = api.get_user('botrobotico')
# print(user.name)

# timeline = api.user_timeline('brunaRuana1')

# HenioBottrel Vnia60277936 Ezequiasns GiffoniCristina
search = '#BolsonaroOrgulhoDoBrasil'
items = 600

accounts = []

def calculate_days_from_now(date):
    """ datetime(year, month, day, hour, minute, second) 
    example date=datetime.datetime(2020, 9, 13, 8, 21, 10)
    """
    today = datetime.datetime.today()     
    c = today-date # returns a timedelta object
    return c.days

def avg_tweets_per_day(total_tweets, days):
    return int(total_tweets/days)
    
    
    



for tweet in tweepy.Cursor(api.search, search).items(items):
    try:
        print(f'@ {tweet.user.screen_name}')

        days = calculate_days_from_now(tweet.user.created_at)
        avg_tweets = avg_tweets_per_day(tweet.user.statuses_count, days)
        if days < 30 or avg_tweets > 200:
            accounts.insert(0, tweet.user.screen_name)
            results.save_account(tweet.user.screen_name)
            print(f'#########\nprovável bot : {tweet.user.name} id: @{tweet.user.screen_name}\n ############')
            print(f'Tweet: {tweet.text}')
            print(f'by: @{tweet.user.screen_name}' )
            print(f'Joined {tweet.user.created_at}')
        
    
        time.sleep(6)
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break