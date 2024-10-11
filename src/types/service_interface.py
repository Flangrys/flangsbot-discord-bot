import abc
import logging


class ServiceInterface(abc.ABC):
    """
    This class represents a basic service.
    A service is understood as any piece of software that encapsulates
    a specific logic that different components of the application
    reuse.
    """

    __logger: logging.Logger = logging.Logger("src.services")

    def __init__(self, *args, **kwargs) -> None:
        pass

    @abc.abstractmethod
    async def setup(self) -> None:
        """
        This method method is used for dependency initialization, check
        validate the internal state or dependencies state, load
        resources, etc.
        """
        pass
