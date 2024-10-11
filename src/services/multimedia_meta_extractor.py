from src.types import service_interface


class MultimediaMetaExtractorService(service_interface.ServiceInterface):
    """ """

    __information_extractor_key: str = "default"

    def __init__(self, *args, **kwargs) -> None: ...

    @property
    def get_info_extractor_key(self) -> str:
        """

        Returns:
            str: the information extractor key.
        """
        return self.__information_extractor_key

    async def __request(self) -> bytes:
        """This method returns the content of the requeted site.

        Returns:
            str: The site content.
        """
        ...

    async def setup_consent(self) -> None:
        """ """
        ...

    async def setup_loging(self) -> None:
        """
        This method will attempt to login into the specific third-part service.
        """
        ...

    def __extract_cookies(self) -> None: ...

    def __normalize_request(self) -> None: ...

    async def setup(self) -> None:

        await self.setup_consent()
        await self.setup_loging()
