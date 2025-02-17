import logging


class DatabaseService:

    def __init__(self) -> None:
        self.__logger = logging.Logger(__name__)
        self.__logger.setLevel(logging.DEBUG)

    async def connect(self): ...

    async def disconnect(self): ...

    async def setup(self):
        self.__logger.info(f"Setting up {__class__} service")


class DatabaseQueryService: ...


class DatabaseMigrationsService: ...


class DatabaseModelManager: ...
