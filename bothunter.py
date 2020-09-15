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
search = '#BolsonaroTemRazao'
items = 1200

results = Result()
bot = BotIdentifier(min_days=30, max_avg_tweets=200)

for tweet in tweepy.Cursor(api.search, search).items(items):
    try:
        print(f'@ {tweet.user.screen_name}')
        
        if bot.analyse_user(tweet.user):
            print('#### ORA ORA')
            results.save_account(tweet.user.screen_name)
            # api.update_status(f'@{tweet.user.screen_name} hmm ', in_reply_to_status_id=tweet.id)
            api.update_status(f'🚨 Alerta! Possível BOT 🚨 \n'
                              f'Usuário @{tweet.user.screen_name}\n'
                              f'Teve uma média de {bot.avg_tweets} Tweets/dia durante seus {bot.days} dias de conta ativa.\n'
                              f'Total de tweets da conta: {tweet.user.statuses_count}\n'
                              f'Termo analisado: {search}')
            print('Tweet Enviado !')            
            print(f'Tweet: {tweet.text}')
            print(f'🚨 Alerta! Possível BOT 🚨 \n'
                  f'Usuário @{tweet.user.screen_name}\n'
                  f'Teve uma média de {bot.avg_tweets} Tweets/dia durante seus {bot.days} dias de conta ativa.\n'
                  f'Total de tweets da conta: {tweet.user.statuses_count}\n'
                  f'Termo analisado: {search}\n\n')
            time.sleep(100)
        
    
        time.sleep(6)
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break