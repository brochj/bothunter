from abc import ABC, abstractmethod
from logging import Logger

import tweepy


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
