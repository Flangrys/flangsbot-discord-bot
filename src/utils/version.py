import typing

type ReleaseType = typing.Literal["release", "candidate", "beta", "indev"]


class ClientVersion(typing.NamedTuple):
    """
    Represents a named versioning tuple which describes the version of this project.
    """

    major: int
    minor: int
    micro: int
    level: ReleaseType
