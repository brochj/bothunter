import logging
import pprint
import time

import tweepy

from bot import Director, HunterBot, HunterBotBuilder
from tools import read_words_list

# hiding these loggers
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("oauthlib").setLevel(logging.WARNING)
logging.getLogger("requests_oauthlib").setLevel(logging.WARNING)
logging.getLogger("tweepy").setLevel(logging.INFO)

TERMS = read_words_list("terms")

bot_hunter: HunterBot = Director.construct_basic_bot(HunterBotBuilder())
bot_hunter.logger.setLevel(logging.DEBUG)

bot_hunter.start(TERMS)


# print(f"Hashtags com termos fornecidos: {matched_hashtags}")
# print(f"Iniciando análise do termo: {term}")

# last_tweeted_message = ""

# for tweet in tweepy.Cursor(api.search_tweets, term).items(items):

#     if tweet.user.screen_name in session.analyzed_accounts:
#         print(
#             f"Esse último usário analisado já foi sobre essa conta.(@ {tweet.user.screen_name})"
#         )
#         print("Passando para o próximo\n\n")
#         time.sleep(2)
#         continue

#     session.add_analyzed_account(tweet.user.screen_name)
#     try:
#         print(f"{session.total_accounts_analyzed()} - @ {tweet.user.screen_name}")

#         if bot.analyse_user(tweet.user):
#             session.add_possible_bot(tweet.user.screen_name)

#             results.save_account(tweet.user.screen_name)
#             tweet_text = (
#                 f"🚨 Alerta! Possível BOT 🚨 \n"
#                 f"Usuário @{tweet.user.screen_name}\n"
#                 f"Teve uma média de {bot.avg_tweets} Tweets/dia durante seus {bot.days} dias de conta ativa.\n"
#                 f"Total de tweets da conta: {tweet.user.statuses_count}\n"
#                 f"Termo analisado: {term}\n\n"
#             )

#             if tweet_text == last_tweeted_message:
#                 print(
#                     f"O último tweet já foi sobre essa conta. (@{tweet.user.screen_name})"
#                 )
#                 print("Passando para o próximo\n\n")
#                 continue

#             last_tweeted_message = tweet_text
#             api.update_status(tweet_text)

#             print("#" * 40 + "\n")
#             print("Tweet Enviado !".center(40))
#             print(tweet_text)

#             time.sleep(100)

#         time.sleep(6)
#     except tweepy.TweepyException as e:
#         print(e.reason)
#     except StopIteration:
#         break
#     except KeyboardInterrupt:
#         print(session)
#         break

# print()
# print()
# print(session)
