import typing


class Service(typing.Protocol):
    """Represents a service."""

    def setup(self) -> None: ...
