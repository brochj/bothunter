# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 20:43:59 2020

@author: broch
"""

import tweepy
import time

import credentials as c
from bot_identifier import BotIdentifier
from bot_actions import BotActions
from save import Result


auth = tweepy.OAuthHandler(c.CONSUMER_KEY, c.CONSUMER_SECRET)
auth.set_access_token(c.ACCESS_TOKEN, c.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

results = Result()
bot = BotIdentifier(api, min_days=30, max_avg_tweets=200)
bot_actions = BotActions(api)

terms = [
    "bolsonaro",
    "jairbolsonaro",
    "bozo",
    "lula",
    "moro",
    "doria",
    "Maia",
    "FlavioBolsonaro",
    "EduardoBolsonaro",
    "presidente",
    "socialismo",
    "capitalismo",
    "comunismo",
    "direita",
    "esquerda",
    "esquerdalha",
    "eleições",
    "urnaeletrônica",
]

matched_hashtags = bot_actions.find_hashtags(terms)

while not matched_hashtags:
    print('Nenhuma Hashtag encontrada, ficarei procurando a cada 15 segundos')
    matched_hashtags = bot_actions.find_hashtags(terms)
    time.sleep(15) # 75 requests/15min
    
search = matched_hashtags[0]
items = 1200

print(f"Hashtags com termos fornecidos: {matched_hashtags}")
print(f"Iniciando análise do termo: {search}")

for tweet in tweepy.Cursor(api.search, search).items(items):
    try:
        print(f"@ {tweet.user.screen_name}")

        if bot.analyse_user(tweet.user):

            print("################################\n")
            results.save_account(tweet.user.screen_name)
            api.update_status(
                f"🚨 Alerta! Possível BOT 🚨 \n"
                f"Usuário @{tweet.user.screen_name}\n"
                f"Teve uma média de {bot.avg_tweets} Tweets/dia durante seus {bot.days} dias de conta ativa.\n"
                f"Total de tweets da conta: {tweet.user.statuses_count}\n"
                f"Termo analisado: {search}"
            )
            print("Tweet Enviado !")
            print(
                f"🚨 Alerta! Possível BOT 🚨 \n"
                f"Usuário @{tweet.user.screen_name}\n"
                f"Teve uma média de {bot.avg_tweets} Tweets/dia durante seus {bot.days} dias de conta ativa.\n"
                f"Total de tweets da conta: {tweet.user.statuses_count}\n"
                f"Termo analisado: {search}\n\n"
            )
            time.sleep(100)
        time.sleep(6)
    except tweepy.TweepError as e:
        print(e.reason)
    except StopIteration:
        break
