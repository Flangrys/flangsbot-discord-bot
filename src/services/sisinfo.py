import logging
import re
import typing

import requests

from src.configuration import environs, loggers


class Metadata(typing.TypedDict):
    payload: dict[str, str]
    headers: dict[str, str]
    cookies: dict[str, str]


class SisinfoService:
    """
    This service provide a set of methods to access
    """

    __SISINFO_LOGIN_URL = "https://sisinfo.unrc.edu.ar/index.php"
    __SISINFO_SITE_URL = "https://sisinfo.unrc.edu.ar/sisinfo/"

    __logger: logging.Logger
    __session: requests.Session
    __current_response: requests.Response | None

    __is_session_active: bool
    __is_session_expired: bool

    __meta: Metadata = {
        "headers": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8",
            "Accept-Language": "es-AR,es;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Origin": "https://sisinfo.unrc.edu.ar",
            "Connection": "keep-alive",
            "Referer": "https://unrc.edu.ar/",
            "User-Agent": "Codemon/0.1.8",
        },
        "cookies": {"sisinfoses1": "", "SisInfo": ""},
        "payload": {
            "f_srv": "2024",
            "FrmCod": "",
            "accion": "entrar",
            "loginUsuario[tipodoc]": "3",
            "loginUsuario[passwd]": "",
            "loginUsuario[codigo]": "",
            "loginUsuario[nrodoc]": "",
        },
    }

    def __init__(self) -> None:
        """Initialize a new SYSINFO Web Scraping Service."""

        self.__logger = loggers.logger("sisinfo")
        self.__logger.setLevel(logging.DEBUG)

        self.__is_session_expired = True
        self.__is_session_active = False

        self.__current_response = None
        """Stores the last response made with the current session."""

    def __check_hard_loging(self, response: requests.Response) -> bool:
        """This method checks if the loging was successful by cheking site metadata.

        Args:
            response (requests.Response): A request response.

        Returns:
            bool: True if the login was successful, False otherwise.
        """

        if not response.ok:
            raise RuntimeError(f"The login request performed at {self.__SISINFO_SITE_URL} fails.")

        elif not response.url == self.__SISINFO_SITE_URL:
            raise RuntimeError(
                f"Unexpected location. Expected: {self.__SISINFO_SITE_URL} but got {response.url}"
            )

        elif (
                self.__session.cookies.get("SisInfo") is None
                or self.__session.cookies.get("sisinfoses1") is None
        ):
            raise RuntimeError(
                f"Missing session cookies. Expected: 'SisInfo' and 'sisinfoses1'"
            )

        return False

    def __get_matched_content(self, expression: re.Pattern, content: str) -> list[str]:
        """Retrieves a list of matched candidates for a given regular expression pattern.

        Args:
            expression (re.Pattern): A regular expression.
            content (str): A string where match.

        Returns:
            list[str]: A list of the possibles candidates.
        """
        return re.findall(expression, content)

    def __grab_session_token(self, content: str) -> str:
        """_summary_

        Args:
            content (str): _description_

        Raises:
            ValueError: _description_
            ValueError: _description_

        Returns:
            str: _description_
        """
        HIDDEN_SESSION_TOKEN = re.compile(
            r'input\s+type=["\']hidden["\']\s+name=["\']FrmCod["\']\s+value=["\'][^"\']*[a-zA-Z0-9][^"\']*["\']'
        )

        candidates: list[str] = []
        candidates_attrs: list[list[str]] = []

        # Matches with a html hidden input with the attribute name set as "FrmCod"
        candidates = self.__get_matched_content(HIDDEN_SESSION_TOKEN, content)

        if len(candidates) < 1:
            raise ValueError("no hidden input with the session token were found")

        # Make a list of tuples which contains the input attributes, with all the candidates.
        candidates_attrs = [candidate.split(" ", 3) for candidate in candidates]

        # Store the session token if exist a candidate with the 'value' attribute.
        tokens: list[str] = []

        for candidates in candidates_attrs:
            for attr in candidates:
                # Ignore this, is not an attribute :)
                if attr == "input":
                    continue

                [key, value] = attr.split("=", 2)
                if key == "value":
                    # Replace the attribute quotation marks with an empty space.
                    normalized_value = value.replace('"', "")

                    tokens.append(normalized_value)

        if len(tokens) == 0:
            raise ValueError("no session token were found")

        return tokens.pop()

    async def login(self) -> None:
        """Attempts to login into 'https://sisinfo.unrc.edu.ar/' site."""

        res: requests.Response

        self.__logger.info("Attempting to request the SISINFO loging site. [INIT]")

        # Login if it's only required.
        if self.__is_session_active and not self.__is_session_expired:
            self.__logger.info("The service is already loggued in.")
            return

        self.__logger.info("Requesting login page content.")

        # Request the login site.
        res = self.__session.get(self.__SISINFO_LOGIN_URL)

        if not res.ok:
            raise RuntimeError(
                f"The request performed at {self.__SISINFO_LOGIN_URL} fails."
            )

        self.__logger.info("Parsing session token.")

        # Parse session token from the requested site content.
        session_token = self.__grab_session_token(res.text)
        document = environs.get_environ("FLANGSBOT_SISINFO_USER_DNI")
        password = environs.get_environ("FLANGSBOT_SISINFO_PASSWORD")

        self.__meta["payload"].update(
            {
                "FrmCod": session_token,
                "loginUsuario[codigo]": session_token,
                "loginUsuario[nrodoc]": document,
                "loginUsuario[passwd]": password,
            }
        )

        self.__meta["headers"].update(
            {"Content-Type": "application/x-www-form-urlencoded"}
        )

        self.__logger.info(f"Attempting to loging with credentials [{session_token}]")

        # Attempting to log in to the site.
        res = self.__session.request(
            "POST",
            url=self.__SISINFO_LOGIN_URL,
            headers=self.__meta.get("headers"),
            data=self.__meta.get("payload"),
        )

        if not self.__check_hard_loging(res):
            raise RuntimeError("Unable to log in to the SISINFO site.")

        self.__logger.info("Loging was successful accomplished [DONE]")

        self.__logger.debug("Storing credentials.")

        # Saving session cookies and configurations.
        self.__meta["cookies"].update(self.__session.cookies)

        self.__is_session_expired = False
        self.__is_session_active = True

    async def logout(self) -> None:
        """Logout from 'https://sisinfo.unrc.edu.ar/' site."""
        self.__logger.warning("Clossing current session")

        self.__is_session_expired = True
        self.__is_session_active = False

        self.__session.close()

    def is_session_expired(self) -> bool:
        return self.__is_session_expired

    def is_session_closed(self) -> bool:
        return not self.__is_session_active

    def check_expiration(self) -> bool:
        return False

    async def req(self, url: str, **kwargs) -> typing.Self:
        if not self.__is_session_active or self.__is_session_expired:
            raise ValueError("Cannot invoke this method before loging.")

        self.__logger.info(f"Requesting at {url}")

        method = kwargs.get("method", "GET")
        self.__current_response = self.__session.request(
            method=method, url=url, **kwargs
        )

        return self

    async def find(self, expression: re.Pattern) -> list[str]:
        if self.__current_response == None:
            raise ValueError("Cannot invoke this method before invoke 'req' method")

        content = self.__current_response.text
        return re.findall(expression, content)

    async def shutdown(self) -> None:
        await self.logout()

    async def setup(self) -> None:
        """Set up the requests session for this service."""
        self.__session = requests.Session()
