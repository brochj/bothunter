# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 20:43:59 2020

@author: broch
"""

import tweepy
import time

import credentials as c
# import functions as f
from bot_identifier import BotIdentifier
from save import Result



auth = tweepy.OAuthHandler(c.CONSUMER_KEY, c.CONSUMER_SECRET)
auth.set_access_token(c.ACCESS_TOKEN, c.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify =True)



# HenioBottrel Vnia60277936 Ezequiasns GiffoniCristina
search = '#BolsonaroOrgulhoDoBrasil'
items = 600

accounts = []
results = Result()
bot = BotIdentifier(min_days=30, max_avg_tweets=200)

for tweet in tweepy.Cursor(api.search, search).items(items):
    try:
        
        
        print(f'@ {tweet.user.screen_name}')

        
        if bot.analyse_user(tweet.user):
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