import base64
import re
from urllib import parse, request


def extract_basic_auth_header(url: str) -> tuple[str, str | None]:
    """This method will return a tuple with the given url and a string with the authentication header.

    Args:
        url (str): A url.

    Returns:
        tuple[str, str | None]: _description_
    """

    # Split the url in their components.
    url_components = parse.urlsplit(url)

    # Check if exist a user with a legit username logged into the website.
    if url_components.username is None:
        return url, None

    url_with_netloc_mutated = url_components._replace(
        netloc=(
            url_components.hostname
            if url_components.port is None
            else f"{url_components.hostname}:{url_components.port}"
        )
    )
    # Combine the splited url components into a new url with
    new_url = parse.urlunsplit(url_with_netloc_mutated)

    # Encode the auth payload.
    auth_payload = base64.b64encode(
        f"{url_components.username}:{url_components.password or ''}".encode("utf-8")
    ).decode("ascii")

    return new_url, f"Basic {auth_payload}"


def update_request(
    request: request.Request,
    url: str | None = None,
    data: dict[str, str] = {},
    headers: dict[str, str] = {},
    query: dict[str, str] = {},
) -> request.Request: ...


COMMON_TYPOS = [
    (r"^httpss://", r"http://"),
    (r"^httpss://", r"http://"),
]
""" Represents a list of tuples with a typo regex template and a fix regex template"""


def sanitize_url_typos(url: str) -> str:
    """
    This function takes an url and will fix a common typing errors in the schema.
    i.e. Given the schema: 'httpp://youtube.com' it will replaced with 'http://youtube.com'.

    Args:
        url (str): A url.

    Returns:
        str: A sanitized url without any typing errors.
    """
    # Prevent scheme-related failures using 'http:' scheme as default.
    if url.startswith("//"):
        return f"http:{url}"

    # Fix the url if there is some common typo pattern.
    for typo, typo_fixup in COMMON_TYPOS:
        # Match the typo.
        if re.match(typo, url):
            # Fix them.
            return re.sub(typo, typo_fixup, url)

    return url


def sanitize_request_auth_header(url: str, **kwargs) -> request.Request:
    # Extract the auth header.
    url, auth_header = extract_basic_auth_header(url)

    headers: dict[str, str]

    if auth_header != None:
        headers = kwargs.get("headers") or {}
        headers["Authorization"] = auth_header

        # Mutate headers before passing it to the Request constructor.
        if kwargs.get("headers") == None:
            kwargs["headers"] = headers

    return request.Request(url, **kwargs)
