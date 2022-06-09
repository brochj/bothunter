# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 20:43:59 2020

@author: broch
"""


import logging
import random
import time
from pprint import pprint

import tweepy

import credentials as c
from bot_actions import BotActions
from bot_identifier import BotIdentifier
from hunting_session import HuntingSession
from save import Result

# from terms import TERMS
from tools import read_words_list

TERMS = read_words_list("terms")

logger = logging.getLogger("bothunter")
logger.setLevel(logging.INFO)
# hiding these loggers
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("oauthlib").setLevel(logging.WARNING)
logging.getLogger("requests_oauthlib").setLevel(logging.WARNING)
logging.getLogger("tweepy").setLevel(logging.INFO)

auth = tweepy.OAuthHandler(c.CONSUMER_KEY, c.CONSUMER_SECRET)
auth.set_access_token(c.ACCESS_TOKEN, c.ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)
results = Result()
bot = BotIdentifier(min_days=30, max_avg_tweets=200)
bot.api = api
bot_actions = BotActions()
bot_actions.api = api


print("#" * 40)
print("Buscando Hashtags que contém um dos seguintes termos")
pprint(TERMS)
matched_hashtags = bot_actions.find_hashtags(TERMS)

while not matched_hashtags:
    print("Nenhuma Hashtag encontrada, ficarei procurando a cada 120 segundos")
    matched_hashtags = bot_actions.find_hashtags(TERMS)
    time.sleep(120)  # 75 requests/15min

term = random.choice(matched_hashtags)
# term = "#Bolsonaro2022"  # just for testing
items = 1800

session = HuntingSession()
session.term = term

print(f"Hashtags com termos fornecidos: {matched_hashtags}")
print(f"Iniciando análise do termo: {term}")

last_tweeted_message = ""

for tweet in tweepy.Cursor(api.search_tweets, term).items(items):

    if tweet.user.screen_name in session.analyzed_accounts:
        print(
            f"Esse último usário analisado já foi sobre essa conta.(@ {tweet.user.screen_name})"
        )
        print("Passando para o próximo\n\n")
        time.sleep(2)
        continue

    session.add_analyzed_account(tweet.user.screen_name)
    try:
        print(f"{session.total_accounts_analyzed()} - @ {tweet.user.screen_name}")

        if bot.analyse_user(tweet.user):
            session.add_possible_bot(tweet.user.screen_name)

            results.save_account(tweet.user.screen_name)
            tweet_text = (
                f"🚨 Alerta! Possível BOT 🚨 \n"
                f"Usuário @{tweet.user.screen_name}\n"
                f"Teve uma média de {bot.avg_tweets} Tweets/dia durante seus {bot.days} dias de conta ativa.\n"
                f"Total de tweets da conta: {tweet.user.statuses_count}\n"
                f"Termo analisado: {term}\n\n"
            )

            if tweet_text == last_tweeted_message:
                print(
                    f"O último tweet já foi sobre essa conta. (@{tweet.user.screen_name})"
                )
                print("Passando para o próximo\n\n")
                continue

            last_tweeted_message = tweet_text
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
    except KeyboardInterrupt:
        print(session)
        break

print()
print()
print(session)
