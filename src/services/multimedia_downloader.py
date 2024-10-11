from src.types import service_interface


class FileDownloaderService(service_interface.ServiceInterface):
    """ """

    def __init__(self, **kwargs) -> None: ...

    async def setup(self) -> None: ...

    async def download(self) -> None: ...
