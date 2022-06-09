import logging
import pprint
import time
from abc import ABC, abstractmethod
from logging import Logger
from typing import Any

import tweepy

import config
import credentials as c
import functions as f
from bot_actions import BotActions
from bot_identifier import BotIdentifier
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
    def start(self, terms) -> None:
        print("I'm not gonna do anything right now")
        self.find_terms_to_analyze(terms)

    def find_terms_to_analyze(self, terms: list[str]) -> list[str]:
        self.logger.info("#" * 40)
        self.logger.info("Buscando Hashtags que contém um dos seguintes termos")
        self.logger.info(terms)
        matched_terms = list()
        while not matched_terms:
            self.logger.info(
                "Nenhuma tesmo encontrado, ficarei procurando a cada 120 segundos"
            )
            trending_topics = self.actions.get_trending_topics()
            matched_terms = self.data_analyzer.find_matched_terms(
                terms,
                trending_topics,
            )
            time.sleep(120)  # 75 requests/15min
        return matched_terms


class HunterBotBuilder(BotBuilder):
    def build_logger(self):
        self.logger = logging.getLogger("bot_hunter")
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
        self.data_analyze = HunterBotDataAnalyzer()
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
        return hashtags

    def extract_trends(self, trending_topics: list[dict]) -> list[str]:
        return trending_topics[0]["trends"]

    def find_matched_terms(self, terms: list[str], trending_topics: list[dict]):
        trends = self.extract_trends(trending_topics)
        matched_terms = [
            ht for term in terms for ht in trends if term.lower() in ht["name"].lower()
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
        # cd3 = self._is_account_age_less_than_minimum_limit(user)
        self._print_bot_analysis(cd1, cd2)
        return cd1 and cd2

    def _analyse_total_tweets(self, user):
        self.avg_tweets = self._avg_tweets_per_day(
            user.statuses_count, self.account_age_days
        )
        self.logger.info(f"avg_tweets:".rjust(36) + f" {self.avg_tweets}")
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

    def _print_bot_analysis(self, cd1: bool, cd2: bool, cd3: bool):
        self.logger.debug(f"Account age:".rjust(36) + f" {self.account_age_days} days")
        self.logger.debug(
            f"avg_tweets > max_avg_tweets ({self.max_avg_tweets}):".rjust(35)
            + f" {cd1}"
        )
        self.logger.debug(f"_is_account_age_less_than_minimum_limit: {cd3}")
        self.logger.debug(f"last_20_tweets_are_retweets:".rjust(35) + f" {cd2}")
