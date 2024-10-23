class MultimediaService:
    """
    This service represents a multimedia information scrapper which is able to
    download and store videos, audio, transcriptions, miniatures, and more
    using only an url or a keyword.
    """

    def __init__(self, *args, **kwargs) -> None: ...

    async def extract_information(
        self, *, download: bool = False, extractor: str = "default"
    ) -> list[dict[str, str]]:
        """Extract the information given by the url and returning a list of
        each extracted video information.

        Args:
            download (bool, optional): True for download the video during the extraction. Defaults to False.
            extractor (str, optional): The extractor key. Defaults to "default".

        Returns:
            list[dict[str, str]]: A list of extracted infomation from each video.
        """
        ...

    async def setup(self) -> None:
        self.__logger.info("[Streaming] Setting up service...")
