import typing

ReleaseLevel: typing.TypeAlias = typing.Literal["release", "candidate", "beta", "indev"]


@typing.final
class ClientVersion(typing.NamedTuple):
    """
    Represents a named versioning tuple wich describes the version of this project.
    """

    major: int
    minor: int
    micro: int
    level: ReleaseLevel
