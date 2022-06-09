import logging
import pprint
import random
import time
from abc import ABC, abstractmethod
from logging import Logger
from typing import Any

import tweepy

import config
import credentials as c
import functions as f
from hunting_session import HuntingSession


class Session(ABC):
    """Store data/stats about the current session"""


class Actions(ABC):
    """This class contains all the methods that interact with the Twitter Api.
    This is where you will extract data and publish tweets"""


class DataAnalyzer(ABC):
    """This class contains all the methods that will analyze and extract useful
    information from the data that was collected by the Actions class."""


class Bot(ABC):
    def __init__(
        self,
        logger: Logger,
        api: tweepy.API,
        session: Session,
        actions: Actions,
        data_analyzer: DataAnalyzer,
    ) -> None:
        self.logger = logger
        self.api = api
        self.session = session
        self.actions = actions
        self.data_analyzer = data_analyzer

    @abstractmethod
    def start(self) -> None:
        pass


class BotBuilder(ABC):
    @abstractmethod
    def build_logger(self):
        return self

    @abstractmethod
    def build_api(self):
        return self

    @abstractmethod
    def build_session(self):
        return self

    @abstractmethod
    def build_actions(self):
        return self

    @abstractmethod
    def build_data_analyzer(self):
        return self

    @abstractmethod
    def get_result(self) -> Bot:
        pass


class Api:
    def __init__(
        self,
        consumer_key: str,
        consumer_secret: str,
        access_token: str,
        access_token_secret: str,
    ) -> None:
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def connect(self) -> tweepy.API:
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

        return tweepy.API(auth)


class HunterBot(Bot):
    def start(self, terms: list[str]) -> None:
        self.logger.info("Ok Boss, let's start the work!!\n")

        term = self.choose_a_term_on_trending_topics(terms)

        tweets = tweepy.Cursor(self.api.search_tweets, term).items(1000)

        for tweet in tweets:
            if self.user_has_been_analyzed(tweet.user.screen_name):
                time.sleep(2)
                continue

            try:
                if self.is_possible_bot(tweet.user):

                    # results.save_account(tweet.user.screen_name)
                    tweet_text = self.create_alert_tweet_message(tweet.user)
                    self.session.last_tweet = tweet_text

                    self.tweet_alert(tweet_text)
                    time.sleep(100)

                time.sleep(6)
            except tweepy.errors.Unauthorized as e:
                self.logger.error(e)
            except tweepy.TweepyException as e:
                print(e)
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
            time.sleep(refresh_seconds)  # 75 requests/15min

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
            self.logger.debug(f"Esse usário (@ {user}) já foi analisado nessa sessão.")
            self.logger.debug("Passando para o próximo...")
        else:
            self.session.add_analyzed_account(user)
        return result

    def is_possible_bot(self, user) -> bool:
        timeline = self.actions.get_user_timeline(user.screen_name)
        result = self.data_analyzer.is_the_user_a_possible_bot(user, timeline)
        if result:
            self.logger.debug(f"@ {user.screen_name} é um possível bot!")
            self.session.add_possible_bot(user.screen_name)
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
        self.actions.tweet(tweet_text)

        self.logger.info("#" * 40 + "\n")
        self.logger.info("Tweet Enviado !".center(40))
        self.logger.info(tweet_text)


class HunterBotBuilder(BotBuilder):
    def build_logger(self):
        self.logger = logging.getLogger("bot_hunter")
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.INFO)
        return self

    def build_api(self):
        self.api = Api(
            c.CONSUMER_KEY, c.CONSUMER_SECRET, c.ACCESS_TOKEN, c.ACCESS_TOKEN_SECRET
        ).connect()
        return self

    def build_session(self):
        self.session = HuntingSession()
        return self

    def build_actions(self):
        self.actions = HunterBotActions()
        self.actions.api = self.api
        return self

    def build_data_analyzer(self):
        self.data_analyze = HunterBotDataAnalyzer(max_avg_tweets=config.MAX_AVG_TWEETS)
        self.data_analyze.logger = self.logger
        return self

    def get_result(self):
        return HunterBot(
            self.logger, self.api, self.session, self.actions, self.data_analyze
        )


class Director:
    @staticmethod
    def construct_basic_bot(bot_builder: BotBuilder):
        return (
            bot_builder.build_logger()
            .build_api()
            .build_session()
            .build_actions()
            .build_data_analyzer()
            .get_result()
        )


class HunterBotActions(Actions):
    def get_trending_topics(self) -> Any:
        """Returns the top 50 trending topics for a specific WOEID, if trending
        information is available for it.

        returns -> [{'as_of': '2022-06-09T01:55:38Z',
                    'created_at': '2022-06-08T08:42:10Z',
                    'locations': [{'name': 'Brazil', 'woeid': 23424768}],
                    'trends': [{'name': 'Flamengo',
                                'promoted_content': None,
                                'query': 'Flamengo',
                                'tweet_volume': 180602,
                                'url': 'http://twitter.com/search?q=Flamengo'},
                                {...},{...},...,{...}]
                    }]
        """
        return self.api.get_place_trends(config.BRAZIL_WOEID)

    def get_home_timeline(self) -> tweepy.models.ResultSet:
        """Returns the 20 most recent statuses, including retweets, posted by
        the authenticating user and that user's friends. This is the equivalent
        of /timeline/home on the Web."""
        return self.api.home_timeline()

    def get_user_timeline(self, screen_name):
        """Returns the 20 most recent statuses posted from the authenticating user
        or the user specified. It's also possible to request another user's
        timeline via the id parameter."""
        return self.api.user_timeline(screen_name=screen_name)

    def tweet(self, text: str):
        self.api.update_status(text)


class HunterBotDataAnalyzer(DataAnalyzer):
    def __init__(self, min_days: int = 30, max_avg_tweets: int = 200):
        self.min_days = min_days
        self.max_avg_tweets = max_avg_tweets
        self.avg_tweets: int = 0
        self.account_age_days: int = 0
        self.user: dict = dict()

    def extract_hashtags(self, trending_topics: list[dict]) -> list[str]:
        trends = self.extract_trends(trending_topics)
        hashtags = [t["name"] for t in trends if t["name"].startswith("#")]
        self.logger.debug(f"hashtags: {hashtags}")
        return hashtags

    def extract_trends(self, trending_topics: list[dict]) -> list[dict]:
        trends = trending_topics[0]["trends"]
        self.logger.debug(f"Trends: {trends}")
        return trends

    def extract_trends_strings(self, trending_topics: list[dict]) -> list[str]:
        trends_dicts = self.extract_trends(trending_topics)
        trends_string = [t["name"] for t in trends_dicts]
        self.logger.info(f"Trends Strings: {trends_string}")
        return trends_string

    def find_matched_terms(self, terms: list[str], trending_topics: list[dict]):
        trends = self.extract_trends_strings(trending_topics)
        matched_terms = [
            ht for term in terms for ht in trends if term.lower() in ht.lower()
        ]
        return matched_terms

    def find_matched_hashtags(self, terms: list[str], trending_topics: list[dict]):
        hashtags = self.extract_hashtags(trending_topics)
        matched_hastags = [
            ht for term in terms for ht in hashtags if term.lower() in ht.lower()
        ]
        return matched_hastags

    def is_the_user_a_possible_bot(self, user, user_timeline) -> bool:
        self.user = user
        self.account_age_days = f.calc_days_until_today(user.created_at)
        cd1 = self._analyse_total_tweets(user)
        cd2 = True | self._is_the_last_20_tweets_are_retweets(user_timeline)
        # cd3 = self.is_the_account_age_less_than_the_minimum_threshold(user)
        self._print_bot_analysis(user, cd1, cd2)
        return cd1 and cd2

    def _analyse_total_tweets(self, user):
        self.avg_tweets = self._avg_tweets_per_day(
            user.statuses_count, self.account_age_days
        )
        return self.avg_tweets > self.max_avg_tweets

    def is_the_account_age_less_than_the_minimum_threshold(self):
        return self.account_age_days < self.min_days

    def _is_the_last_20_tweets_are_retweets(self, user_timeline):
        return all(hasattr(item, "retweeted_status") for item in user_timeline)

    def _avg_tweets_per_day(self, total_tweets, days):
        try:
            return int(total_tweets / days)
        except ZeroDivisionError:
            return total_tweets

    def _print_bot_analysis(self, user, cd1: bool, cd2: bool, cd3: bool = False):
        tweets_total = f"{user.statuses_count:,}".replace(",", ".")
        username = f"@ {user.screen_name}"
        account_age = f"{self.account_age_days}"

        colunm_size = 20  # min 20

        self.logger.info(
            username.rjust(colunm_size)
            + " | "
            + (f"{self.avg_tweets}".rjust(4) + f" tweets/day").center(colunm_size)
            + " | "
            + (tweets_total.rjust(11) + " Tweets").center(colunm_size)
            + " | "
            + (account_age.rjust(4) + " days (acc age)").center(colunm_size)
            + " | "
        )

        max_str = 45

        self.logger.debug("-" * max_str * 2)
        self.logger.debug(
            f"Account age: ".rjust(max_str) + f"{self.account_age_days} days"
        )
        self.logger.debug(
            f"Tweets Total: ".rjust(max_str)
            + f"{user.statuses_count:,}".replace(",", ".")
        )
        self.logger.debug(
            f"Average Tweets: ".rjust(max_str) + f"{self.avg_tweets} tweets/day"
        )
        self.logger.debug(
            f"Avg. Tweets > Max Avg. Tweets ({self.max_avg_tweets}): ".rjust(max_str)
            + str(cd1)
        )
        # self.logger.debug(f"is_the_account_age_less_than_the_minimum_threshold: {cd3}")
        # self.logger.debug(f"last_20_tweets_are_retweets: ".rjust(max_str) + str(cd2))
        self.logger.debug("-" * max_str * 2)
