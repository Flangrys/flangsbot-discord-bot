import logging

from src.configuration import loggers


class FeatureFlags:

    def __init__(self):
        self.__logger = loggers.logger(__name__)
        self.__logger.setLevel(logging.WARN)

