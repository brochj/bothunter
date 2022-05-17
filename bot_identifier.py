# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 13:45:22 2020

@author: broch
"""
import functions as f
import logging

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger("Account_info")
logger.setLevel(logging.WARNING)


class BotIdentifier:
    def __init__(self, api, min_days, max_avg_tweets):
        self.api = api
        self.min_days = min_days
        self.max_avg_tweets = max_avg_tweets
        self.avg_tweets = 0
        self.days = 0
        self.user = {}

    def analyse_user(self, user):
        self.user = user
        self.days = f.calculate_days_from_now(user.created_at)
        cd1 = self._analyse_total_tweets(user)
        cd2 = True | self._last_20_tweets_are_retweets()
        # cd3 = self._analyse_created_at(user)
        logger.info(f"Account age:".rjust(36) + f" {self.days} days")
        logger.debug(
            f"avg_tweets > max_avg_tweets ({self.max_avg_tweets}):".rjust(35)
            + f" {cd1}"
        )
        logger.debug(f"last_20_tweets_are_retweets:".rjust(35) + f" {cd2}")
        return cd1 and cd2

    def _analyse_total_tweets(self, user):
        self.avg_tweets = self._avg_tweets_per_day(user.statuses_count, self.days)
        logger.info(f"avg_tweets:".rjust(36) + f" {self.avg_tweets}")
        return self.avg_tweets > self.max_avg_tweets

    def _analyse_created_at(self, user):
        return self.days < self.min_days

    def _last_20_tweets_are_retweets(self):
        timeline = self.api.user_timeline()
        return all(hasattr(item, "retweeted_status") for item in timeline)

    def _avg_tweets_per_day(self, total_tweets, days):
        try:
            return int(total_tweets / days)
        except ZeroDivisionError:
            return total_tweets
