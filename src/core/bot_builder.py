from abc import ABC, abstractmethod

from src.core.bot import Bot


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
