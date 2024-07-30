import logging
import re

import requests

from src.services import abc


class SYSINFOService(abc.AbstractService):
    """
    This class represents a web scrapping service that collects information
    from the site: "sisinfo.unrc.edu.ar".
    """

    __logger: logging.Logger
    __response: requests.Response

    __sisinfo_user_dni: str
    __sisinfo_user_passwd: str

    __sisinfo_request_url: str = "https://sisinfo.unrc.edu.ar/"
    __sisinfo_request_params: list[str] = [
        "accion=entrar",
        "gencook=",
        "FrmCod=",
        "f_srv=2024",
        "loginUsuario[codigo]=",
        "loginUsuario[tipodoc]=3",
        "loginUsuario[nrodoc]=",
        "loginUsuario[passwd]=",
        "ingresar=",
    ]
    __sisinfo_request_headers: list[str] = [
        "Referer https://sisinfo.unrc.edu.ar/sisinfo/",
    ]
    __sisinfo_request_cookies: list[str] = ["sisinfoses1=", "SisInfo="]

    __is_client_logged: bool
    """Represents a binary state for the user logging state."""

    __is_client_loaded: bool
    """Represents a binary state for the user logging site state."""

    def __init__(self) -> None:
        """Initialize a new SYSINFO Web Scraping Service.

        Raises:
            RuntimeError: When an environ variable were missing.
        """
        self.__logger = logging.getLogger("discord")

        self.__is_client_logged = False
        self.__is_client_loaded = False

    @property
    def response(self) -> requests.Response:
        return self.__response

    def __format_params(self):
        for param in self.__sisinfo_request_params:
            subparams = param.split("=", 2)
            yield subparams[0], subparams[1]

    def __format_headers(self):
        for header in self.__sisinfo_request_headers:
            subheaders = header.split(" ", 2)
            yield subheaders[0], subheaders[1]

    def __format_cookies(self):
        for cookie in self.__sisinfo_request_cookies:
            subcookies = cookie.split("=", 2)
            yield subcookies[0], subcookies[1]

    def __build_request_body(self):

        params = {key: value for key, value in self.__format_params()}
        headers = {key: value for key, value in self.__format_headers()}
        cookies = {key: value for key, value in self.__format_cookies()}

        params["FrmCod"] = self.__extract_session_code()
        params["loginUsuario[codigo]"] = self.__extract_session_code()
        params["loginUsuario[nrodoc]"] = self.__sisinfo_user_dni
        params["loginUsuario[passwd]"] = self.__sisinfo_user_passwd

        # cookies["sisinfoses1"]=
        # cookies["SisInfo"]=

        return params, headers, cookies

    @property
    def session_token(self) -> str:
        return self.__response.headers["sisinfoses1"]

    def __extract_session_code(self) -> str:
        """This method extracts the FormCode that represents a session token.
        This token is used each time the user tries to login.

        Raises:
            ValueError: When the session code input is missing.

        Returns:
            str: The session token.
        """
        match_form_session_code_input = re.compile(
            r'input\s+type=["\']hidden["\']\s+name=["\']FrmCod["\']\s+value=["\'][^"\']*[a-zA-Z0-9][^"\']*["\']'
        )

        self.__logger.debug("[extract_session_code] Extracting session token.")

        session_codes_matched = self.parse_content(match_form_session_code_input)

        if len(session_codes_matched) < 1:
            raise ValueError(
                "the hidden formulary input for the session code is missing."
            )

        self.__logger.debug("[session_code] Extracting session code.")

        session_code = session_codes_matched[0].split(" ", 2)

        session_code = session_code[2].split("=", 2)[1]

        self.__logger.info(
            "[extract_session_code] Sucssesfully extracted the session code: %s",
            session_code,
        )

        return session_code.replace('"', "")

    def parse_content(self, pattern: re.Pattern[str] | str) -> list[str]:
        """Given a compiled pattern or a string, this method will return
         a list of the templates that matches with the given patter.

        Args:
            pattern (re.Pattern[str] | str): An expresion that will match with a specific content.

        Returns:
            list[str]: A list of all matches in the response content.
        """

        content = self.__response.content.decode("utf-8", "replace")

        return re.findall(pattern, content)

    def request_index(self) -> None:
        """This method will request the initial resources required to logging to the site.

        Raises:
            ConnectionError: When the external server does not responds as expected.
        """
        url = self.__sisinfo_request_url

        self.__logger.debug("[request_index] Requesting an initial resource at %s", url)

        initial_response = requests.request("GET", url=url)

        if not initial_response.ok:
            raise ConnectionError(
                f"The server {url} respond with a {initial_response.status_code} code wich is not an expected reponse code."
            )

        self.__response = initial_response
        self.__is_client_loaded = True
        self.__logger.info(
            "[request_index] The initial resource request at %s was successfuly requested",
            url,
        )

    def request_loging(self) -> None:
        """This method will request a logging action to the logging site.

        Raises:
            ConnectionError: When the external server does not responds as expected.
        """

        url = self.__sisinfo_request_url

        loging_params, loging_headers, loging_cookies = self.__build_request_body()

        self.__logger.debug(
            "[request_loging] Requesting a loging at %s as %s",
            url,
            self.__sisinfo_user_dni,
        )

        # HERE: Request logging.
        loging_response = requests.request(
            "POST",
            url=url,
            params=loging_params,
            headers=loging_headers,
            cookies=loging_cookies,
        )

        if not loging_response.ok:
            raise ConnectionError(
                f"The server {url} respond with a {loging_response.status_code} code wich is not an expected response code."
            )

        if (
            not loging_response.status_code == 302
            or loging_response.headers.get("location") == None
        ):
            raise ConnectionError(
                f"the server {url} denied the access to this resource."
            )

        self.__response = loging_response
        self.__is_client_logged = True
        self.__logger.info(
            "[request_loging] The loging request at %s was successfully requested",
            url,
        )

    async def setup(self) -> None:
        """This method will setup a connection with the remote server.

        Raises:
            ConnectionError: When the external server does not respond as expected.
        """

        # TODO []: Check if a current session still exist.
        # TODO []: Check if the session has expired.

        # HERE: Request initial resources.
        self.request_index()

        # HERE: Request logging action.
        self.request_loging()

    def request_resource(self, url: str) -> None:

        if not (self.__is_client_loaded and self.__is_client_logged):
            raise SystemError("cannot request a resource until login into the site.")

        request_params, request_headers, request_cookies = self.__build_request_body()

        self.__logger.debug("[request_resource] Requesting a resource at %s", url)

        response = requests.request(
            "GET",
            url=url,
            params=request_params,
            headers=request_headers,
            cookies=request_cookies,
        )

        if not self.__response.ok:
            raise ConnectionError(
                "the remote server responded respond with does not respond as expect."
            )

        self.__response = response
        self.__logger.info(
            "[request_resource] The resource was successfully requested."
        )
