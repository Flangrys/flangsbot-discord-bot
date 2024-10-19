import typing


class SisinfoRequest(typing.TypedDict):
    payload: dict[str, str]
    headers: dict[str, str]
    cookies: dict[str, str]
