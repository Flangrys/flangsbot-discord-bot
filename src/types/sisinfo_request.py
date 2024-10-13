import typing


class SisinfoRequest(typing.TypedDict):
    url: str
    payload: dict[str, str]
    headers: dict[str, str]
    cookies: dict[str, str]
