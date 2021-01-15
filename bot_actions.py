# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 17:06:29 2020

@author: broch
"""


class BotActions:

    def __init__(self, api):
        self.api = api

    def find_hashtags(self, terms, location=23424768):
        # BRAZIL_WOEID = 23424768
        trends = self.api.trends_place(location)
        hashtags = [t["name"] for t in trends[0]["trends"] if t["name"].startswith("#")]
        matched_hashtags = [
            ht for term in terms for ht in hashtags if term.lower() in ht.lower()
        ]
        return matched_hashtags
