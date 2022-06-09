from bot import Director, HunterBot, HunterBotBuilder
from tools import read_words_list

# hiding these loggers
# logging.getLogger("urllib3").setLevel(logging.WARNING)
# logging.getLogger("oauthlib").setLevel(logging.WARNING)
# logging.getLogger("requests_oauthlib").setLevel(logging.WARNING)
# logging.getLogger("tweepy").setLevel(logging.INFO)

TERMS = read_words_list("terms")

bot_hunter: HunterBot = Director.construct_basic_bot(HunterBotBuilder())

bot_hunter.start(TERMS)
