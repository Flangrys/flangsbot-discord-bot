import logging
import re

import requests

from src.configuration import environs, loggers
from src.types import service_interface
from src.types.sisinfo_request import SisinfoRequest


class SYSINFOService(service_interface.ServiceInterface):
    """
    This service provide a set of methods to access
    """

    __SISINFO_URL = "https://sisinfo.unrc.edu.ar/sisinfo/"

    __logger: logging.Logger
    __session: requests.Session

    __meta: SisinfoRequest = {
        "url": "https://sisinfo.unrc.edu.ar/index.php",
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

    __is_logged: bool
    __is_expired: bool

    def __init__(self) -> None:
        """Initialize a new SYSINFO Web Scraping Service."""

        self.__logger = loggers.logger("sisinfo")
        self.__logger.setLevel(logging.DEBUG)

        self.__is_expired = True
        self.__is_logged = False

    def __get_matched_content(self, expression: re.Pattern, content: str) -> list[str]:
        return re.findall(expression, content)

    def __grab_session_token(self, content: str) -> str:
        HIDDEN_SESSION_TOKEN = re.compile(
            r'input\s+type=["\']hidden["\']\s+name=["\']FrmCod["\']\s+value=["\'][^"\']*[a-zA-Z0-9][^"\']*["\']'
        )

        candidates: list[str] = []
        candidates_attrs: list[list[str]] = []

        # Matches with an html hidden input with the attribute name set as "FrmCod"
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

        self.__logger.info("Attempting to request the SISINFO loging site.")

        # Login if it's only required.
        if self.__is_logged and not self.__is_expired:
            self.__logger.info("The service is already loggued in.")
            return

        self.__logger.info("Requesting login page content")

        URL = self.__meta.get("url")

        # Request the login site.
        res = self.__session.get(URL)

        if not res.ok:
            raise RuntimeError(f"The request performed at {URL} fails.")

        self.__logger.info("Parsing session token")

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

        self.__logger.info(f"attempting to loging with credentials [{session_token}]")

        # Attempting to login into the site.
        res = self.__session.request(
            "POST",
            url=URL,
            headers=self.__meta.get("headers"),
            data=self.__meta.get("payload"),
        )

        if not res.ok:
            raise RuntimeError(f"The login request performed at {URL} fails.")

        elif not res.url == self.__SISINFO_URL:
            raise RuntimeError(
                f"Unexpected location. Expected: {self.__SISINFO_URL} but got {res.url}"
            )

        elif (
            self.__session.cookies.get("SisInfo") == None
            or self.__session.cookies.get("sisinfoses1") == None
        ):
            raise RuntimeError(
                f"Missing session cookies. Expected: 'SisInfo' and 'sisinfoses1'"
            )

        self.__logger.info("LOGING WAS SUCCESSFULLY ACCOMPLISHED! YUPIII.")

        self.__logger.debug("Storing credentials.")

        # Saving session cookies and configurations.
        self.__meta["cookies"].update(self.__session.cookies)

        self.__is_expired = False
        self.__is_logged = True

    async def logout(self) -> None:
        """Logout from 'https://sisinfo.unrc.edu.ar/' site."""
        self.__logger.warning("Clossing current session")

        self.__is_expired = True
        self.__is_logged = False

        self.__session.close()

    def is_session_expired(self) -> bool:
        return self.__is_expired

    def is_session_closed(self) -> bool:
        return not self.__is_logged

    async def setup(self) -> None:
        """Setup the requests session for this service."""
        self.__session = requests.Session()
