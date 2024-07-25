import typing


class SYSINFORequest(typing.TypedDict):
    url: str
    params: list[str]
    headers: list[str]
    cookies: list[str]
