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
    @abstractmethod
    def start(self) -> None:
        pass
