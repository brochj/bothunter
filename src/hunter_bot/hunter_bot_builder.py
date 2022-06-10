import logging

import configs.config as config
import configs.credentials as credentials
from src.core.api import Api
from src.core.bot_builder import BotBuilder
from src.hunter_bot.hunter_bot import HunterBot
from src.hunter_bot.hunter_bot_actions import HunterBotActions
from src.hunter_bot.hunter_bot_data_analyzer import HunterBotDataAnalyzer
from src.hunter_bot.hunting_session import HuntingSession


class HunterBotBuilder(BotBuilder):
    def build_logger(self):
        self.logger = logging.getLogger("bot_hunter")
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.INFO)
        return self

    def build_api(self):
        self.api = Api(
            credentials.CONSUMER_KEY,
            credentials.CONSUMER_SECRET,
            credentials.ACCESS_TOKEN,
            credentials.ACCESS_TOKEN_SECRET,
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
        self.data_analyzer = HunterBotDataAnalyzer(max_avg_tweets=config.MAX_AVG_TWEETS)
        self.data_analyzer.logger = self.logger
        return self

    def get_result(self):
        return HunterBot(
            self.logger, self.api, self.session, self.actions, self.data_analyzer
        )
