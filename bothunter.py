from src.core.bot_builder import Director
from src.hunter_bot.hunter_bot import HunterBot
from src.hunter_bot.hunter_bot_builder import HunterBotBuilder
from src.utils.file import read_words_list

TERMS = read_words_list("terms")

bot_hunter: HunterBot = Director.construct_basic_bot(HunterBotBuilder())

bot_hunter.start(TERMS)
