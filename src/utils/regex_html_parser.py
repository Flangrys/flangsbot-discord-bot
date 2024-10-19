import re

from src.utils.regex_html import Element


class RegexHTMLParser:
    """Provides a set of methods for HTML element processing."""

    __text: str

    def __init__(self, text: str) -> None:
        self.__text = text

    def to_dict(self) -> Element:
        """Retrieves a dictionary with the elements that compound the html tag.

        Returns:
            Element: A typed dictionary with the tag elements.
        """
        ...

    def zip(self) -> set[Element]:
        """Retrieves a set of the elements contained in the current text.

        Returns:
            set[Element]: A set of the found elements
        """
        ...
