import random
import sqlite3
import time
from datetime import datetime
from logging import Logger
from pprint import pprint

import tweepy
from src.core.bot import Bot
from src.core.user import User
from src.hunter_bot.hunter_bot_actions import HunterBotActions
from src.hunter_bot.hunter_bot_data_analyzer import HunterBotDataAnalyzer
from src.hunter_bot.hunter_bot_writer import UserSqlite
from src.hunter_bot.hunting_session import HuntingSession
from src.utils.utils import wait_secs


class HunterBot(Bot):
    def __init__(
        self,
        logger: Logger,
        api: tweepy.API,
        session: HuntingSession,
        actions: HunterBotActions,
        data_analyzer: HunterBotDataAnalyzer,
        writer: UserSqlite,
    ) -> None:
        self.logger = logger
        self.api = api
        self.session = session
        self.actions = actions
        self.data_analyzer = data_analyzer
        self.user: User
        self.writer = writer

    def create_user(self, tweepy_user):
        return User(
            id=tweepy_user.id,
            id_str=tweepy_user.id_str,
            name=tweepy_user.name,
            screen_name=tweepy_user.screen_name,
            location=tweepy_user.location,
            url=tweepy_user.url,
            description=tweepy_user.description,
            protected=tweepy_user.protected,
            verified=tweepy_user.verified,
            followers_count=tweepy_user.followers_count,
            friends_count=tweepy_user.friends_count,
            listed_count=tweepy_user.listed_count,
            favourites_count=tweepy_user.favourites_count,
            statuses_count=tweepy_user.statuses_count,
            created_at=tweepy_user.created_at,
            profile_banner_url=tweepy_user.profile_banner_url
            if hasattr(tweepy_user, "profile_banner_url")
            else "",
            profile_image_url_https=tweepy_user.profile_image_url_https,
            default_profile=tweepy_user.default_profile,
            default_profile_image=tweepy_user.default_profile_image,
            first_scrape=datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        )

    def start(self, terms: list[str]) -> None:
        self.logger.info("Ok Boss, let's start the work!!\n")

        term = self.choose_a_term_on_trending_topics(terms)

        tweets = tweepy.Cursor(self.api.search_tweets, term).items(1000)

        for tweet in tweets:
            if self.user_has_been_analyzed(tweet.user.screen_name):
                wait_secs(4)
                continue

            self.user = self.create_user(tweet.user)
            try:
                self.writer.save(self.user)
            except sqlite3.IntegrityError:
                # TODO create update user
                self.logger.info(
                    "Esse usuário já está no banco de dados...passando para o próximo"
                )

            try:
                if not self.is_possible_bot(tweet.user):
                    wait_secs(6)
                    continue

                # results.save_account(tweet.user.screen_name)
                tweet_text = self.create_alert_tweet_message(tweet.user)

                # Prevent duplicate tweet
                if self.session.last_tweet == tweet_text:
                    self.logger.info("Último tweet enviado é igual...não vou tweetar")
                    wait_secs(6)
                    continue

                self.session.last_tweet = tweet_text
                self.tweet_alert(tweet_text)
                wait_secs(100)

            except tweepy.errors.Unauthorized as e:
                # User has blocked the bot
                self.logger.error(e)
                break

                # Twitter blocks the bot
                # 261 - Application cannot perform write actions.
                # Contact Twitter Platform Operations through https://help.twitter.com/forms/platform.
            except tweepy.TweepyException as e:
                self.logger.error(e)
                break
            except StopIteration:
                break
            except KeyboardInterrupt:
                print(self.session)
                break

    def choose_a_term_on_trending_topics(self, terms: list[str]):
        matched_terms = self.find_terms_to_analyze(terms)
        return self.pick_one(matched_terms)

    def find_terms_to_analyze(
        self, terms: list[str], refresh_seconds: int = 120
    ) -> list[str]:
        self.logger.info("#" * 40)
        self.logger.info("Buscando Trends que contém um dos seguintes termos")
        self.logger.info(terms)
        matched_terms = []
        while True:
            trending_topics = self.actions.get_trending_topics()
            matched_terms = self.data_analyzer.find_matched_terms(
                terms,
                trending_topics,
            )
            if matched_terms:
                break

            self.logger.info(
                f"Nenhum termo encontrado, vou a procurar daqui a {refresh_seconds} segundos"
            )
            wait_secs(refresh_seconds)  # 75 requests/15min

        self.logger.info(f"Termos encontrados: {matched_terms}")
        return matched_terms

    def pick_one(self, terms: list[str]) -> str:
        choosed = random.choice(terms)
        self.logger.info(f"Termo escolhido: {choosed}")
        self.session.term = choosed
        return choosed

    def user_has_been_analyzed(self, user: str) -> bool:
        result = user in self.session.analyzed_accounts
        if result:
            self.logger.debug(
                f"Esse usário (@ {user}) já foi analisado nessa sessão...passando para o próximo"
            )
        else:
            self.session.add_analyzed_account(user)
        return result

    def is_possible_bot(self, user) -> bool:
        self.logger.debug(f"Checando se @ {user.screen_name} é um bot...")
        # timeline = self.actions.get_user_timeline(user.screen_name)
        result = self.data_analyzer.is_the_user_a_possible_bot(
            user, "change_here", check_timeline=False, check_account_age=False
        )
        if result:
            self.logger.debug(f"@ {user.screen_name} é um possível bot!")
            self.session.add_possible_bot(user.screen_name)
        else:
            self.logger.debug(f"@ {user.screen_name} não é um bot...")
        return result

    def create_alert_tweet_message(self, user) -> str:
        message = (
            f"🚨 Alerta! Possível BOT 🚨 \n"
            f"Usuário @{user.screen_name}\n"
            f"Teve uma média de {self.data_analyzer.avg_tweets} Tweets/dia durante seus {self.data_analyzer.account_age_days} dias de conta ativa.\n"
            f"Total de tweets da conta: {user.statuses_count:,}".replace(",", ".")
            + "\n"
            f"Termo analisado: {self.session.term}\n\n"
        )
        return message

    def tweet_alert(self, tweet_text: str) -> None:
        self.logger.info("#" * 40)
        self.logger.info("Tweet sent !".center(40))
        self.logger.info(tweet_text)
        self.logger.info("#" * 40)

        self.actions.tweet(tweet_text)
