from typing import Any

import configs.config as config
import tweepy
from src.core.bot import Actions


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
