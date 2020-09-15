# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 13:45:22 2020

@author: broch
"""
import functions as f


class BotIdentifier:
    
    def __init__(self, min_days, max_avg_tweets):
        self.min_days = min_days
        self.max_avg_tweets = max_avg_tweets
        self.avg_tweets = 0
        self.days = 0

    
    def analyse_user(self, user):
        self.days = f.calculate_days_from_now(user.created_at)
        cd1 = self.__analyse_total_tweets(user)
        # cd2 = self.__analyse_created_at(user)
        return cd1
    
    def __analyse_total_tweets(self, user):
        self.avg_tweets = self.avg_tweets_per_day(user.statuses_count, self.days)
        return self.avg_tweets > self.max_avg_tweets


    def __analyse_created_at(self, user):
        return self.days < self.min_days
         
        
    def avg_tweets_per_day(self, total_tweets, days):
        try:
            return int(total_tweets/days)
        except ZeroDivisionError:
            return total_tweets