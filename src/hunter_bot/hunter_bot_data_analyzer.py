import src.utils.utils as utils
from src.core.bot import DataAnalyzer


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

    def is_the_user_a_possible_bot(
        self,
        user,
        user_timeline,
        check_avg_tweets=True,
        check_timeline=True,
        check_account_age=True,
    ) -> bool:
        self.user = user
        self.account_age_days = utils.calc_days_until_today(user.created_at)

        cd_avg_tweets = False
        cd_last_20 = False
        cd_acc_age = False

        if check_avg_tweets:
            cd_avg_tweets = self._analyze_avg_tweets(user)

        if check_timeline:
            cd_last_20 = self._is_the_last_20_tweets_are_retweets(user_timeline)

        if check_account_age:
            cd_acc_age = self.is_the_acc_age_less_than_the_minimum_threshold(user)

        self._print_bot_analysis(user)

        if check_avg_tweets and check_timeline and check_account_age:
            return cd_avg_tweets and cd_last_20 and cd_acc_age
        if check_avg_tweets and check_timeline:
            return cd_avg_tweets and cd_last_20
        if check_avg_tweets:
            return cd_avg_tweets

    def _analyze_avg_tweets(self, user):
        self.avg_tweets = self._avg_tweets_per_day(
            user.statuses_count, self.account_age_days
        )
        return self.avg_tweets > self.max_avg_tweets

    def is_the_acc_age_less_than_the_minimum_threshold(self):
        return self.account_age_days < self.min_days

    def _is_the_last_20_tweets_are_retweets(self, user_timeline):
        return all(hasattr(item, "retweeted_status") for item in user_timeline)

    def _avg_tweets_per_day(self, total_tweets, days):
        try:
            return int(total_tweets / days)
        except ZeroDivisionError:
            return total_tweets

    def _print_bot_analysis(self, user):
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
