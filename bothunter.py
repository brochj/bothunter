# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 20:43:59 2020

@author: broch
"""


from pprint import pprint
import logging
import random
import time
import tweepy

from bot_actions import BotActions
from bot_identifier import BotIdentifier
from save import Result
from terms import TERMS
import credentials as c

logger = logging.getLogger()
logger.setLevel(logging.INFO)

auth = tweepy.OAuthHandler(c.CONSUMER_KEY, c.CONSUMER_SECRET)
auth.set_access_token(c.ACCESS_TOKEN, c.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
results = Result()
bot = BotIdentifier(api, min_days=30, max_avg_tweets=200)
bot_actions = BotActions(api)

print("#" * 40)
print("Buscando Hashtags que contém um dos seguintes termos")
pprint(TERMS)
matched_hashtags = bot_actions.find_hashtags(TERMS)

while not matched_hashtags:
    print("Nenhuma Hashtag encontrada, ficarei procurando a cada 30 segundos")
    matched_hashtags = bot_actions.find_hashtags(TERMS)
    time.sleep(30)  # 75 requests/15min

term = random.choice(matched_hashtags)
# term = "#Bolsonaro2022"  # just for testing
items = 1800

print(f"Hashtags com termos fornecidos: {matched_hashtags}")
print(f"Iniciando análise do termo: {term}")

for tweet in tweepy.Cursor(api.search_tweets, term).items(items):
    try:
        print(f"@ {tweet.user.screen_name}")

        if bot.analyse_user(tweet.user):

            results.save_account(tweet.user.screen_name)
            tweet_text = (
                f"🚨 Alerta! Possível BOT 🚨 \n"
                f"Usuário @{tweet.user.screen_name}\n"
                f"Teve uma média de {bot.avg_tweets} Tweets/dia durante seus {bot.days} dias de conta ativa.\n"
                f"Total de tweets da conta: {tweet.user.statuses_count}\n"
                f"Termo analisado: {term}\n\n"
            )
            api.update_status(tweet_text)

            print("#" * 40 + "\n")
            print("Tweet Enviado !".center(40))
            print(tweet_text)

            time.sleep(100)

        time.sleep(6)
    except tweepy.TweepyException as e:
        print(e.reason)
    except StopIteration:
        break
