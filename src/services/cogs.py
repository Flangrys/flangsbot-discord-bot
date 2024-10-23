import pathlib
import typing

from discord.ext import commands

class Extension(typing.TypedDict):
    name: str
    """The extension name."""

    package: str
    """The extension package path."""

    enabled: bool
    """True if the extension is enabled, False otherwise."""


class CogsService:
    COGS_MAP: dict[str, int]
    COGS: list[Extension]
    COGS_PATHS: list[pathlib.Path]

    def __init__(self, bot: commands.Bot) -> None:
        self.__bot = bot

        self.COGS_MAP = {}
        self.COGS = []
        self.COGS_PATHS = [
            path for path in self.get_extensions_path().glob("*.py")
        ]

        for index in range(len(self.COGS_PATHS)):
            self.COGS_MAP.update({self.COGS_PATHS[index].stem: index})
            self.COGS.append(
                {
                    "name": self.COGS_PATHS[index].stem,
                    "package": self.COGS_PATHS[index].name,
                    "enabled": False,
                }
            )

    async def setup(self) -> None:
        await self.load_all_extensions()

    @staticmethod
    def get_extensions_path() -> pathlib.Path:
        return pathlib.Path(__file__).parent.parent / "extensions"

    def is_extension_loaded(self, extension: str) -> bool:
        """Check if an extension is loaded.

        Args:
            extension (str): The extension string import path

        Returns:
            bool: True if it is loaded.
        """

        index = self.COGS_MAP[extension]
        return self.COGS[index]["enabled"]

    def is_all_extensions_loaded(self) -> bool:
        """This method returns true when all the extensions are loaded.

        Returns:
            bool: True when all extensions are loaded, False otherwise.
        """

        return all([ext["enabled"] for ext in self.COGS] or [False])

    async def load_extension(self, extension: str) -> None:
        """This method loads an extension given by their path.

        Args:
            extension (str): The extension path.

        Raises:
            ValueError: When the extension is already loaded.
        """

        if extension not in self.COGS_MAP:
            raise ValueError(
                f"the extension {extension} does not exist in the extensions path"
            )

        if self.is_extension_loaded(extension):
            raise ValueError(f"the extension {extension} is already loaded")

        __extension = self.COGS_MAP[extension]
        self.COGS[__extension]["enabled"] = True

        full_extension_name = "src.extensions." + extension

        await self.__bot.load_extension(full_extension_name)

    async def load_all_extensions(self) -> None:
        """This method loads all the existing extensions in the extensions path.

        Raises:
            ValueError: When some extension is already loaded.
        """

        if self.is_all_extensions_loaded():
            raise ValueError("cannot load all the extensions that it is already loaded")

        for extension in self.COGS_MAP:
            await self.load_extension(extension)

    async def unload_extension(self, extension: str) -> None:
        """This method unload an extension given by their path.

        Args:
            extension (str): The extension path.

        Raises:
            ValueError: When the extension is already unloaded.
        """

        if extension not in self.COGS_MAP:
            raise ValueError(
                f"the extension {extension} does not exist in the extensions path"
            )

        if not self.is_extension_loaded(extension):
            raise ValueError(f"the extension {extension} is already unloaded")

        __extension = self.COGS_MAP[extension]
        self.COGS[__extension]["enabled"] = False

        full_extension_name = "src.extensions." + extension

        await self.__bot.unload_extension(full_extension_name)

    async def unload_all_extension(self) -> None:
        """This method unloads all the existing extensions in the extension path.

        Raises:
            ValueError: When some extension is already unloaded.
        """
        if not self.is_all_extensions_loaded():
            raise ValueError(
                "cannot unload all the extensions that it is already unloaded"
            )

        for extension in self.COGS_MAP:
            await self.unload_extension(extension)

    def get_enabled_extensions(self) -> list[str]:
        enabled_extensions: list[str] = []

        for ext in self.COGS:
            if ext["enabled"]:
                enabled_extensions.append(ext["name"])

        return enabled_extensions
