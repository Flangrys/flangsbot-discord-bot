import typing


class Extension(typing.TypedDict):
    name: str
    """The extension name."""

    package: str
    """The extension package path."""

    enabled: bool
    """True if the extension is enabled, False otherwise."""
