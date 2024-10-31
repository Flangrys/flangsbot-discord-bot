import logging

from src.configuration import loggers


class MultimediaService:
    """
    This service represents a multimedia information scrapper which is able to
    download and store videos, audio, transcriptions, miniatures, and more
    using only an url or a keyword.
    """

    def __init__(self, *args, **kwargs) -> None:
        self.__logger = loggers.logger(__name__)
        self.__logger.setLevel(logging.WARN)

    async def setup(self) -> None:
        self.__logger.info("[Streaming] Setting up service...")
