import pathlib
from logging import Logger

from discord.ext import commands

from src.configuration import loggers
from src.utils.extension import Extension


class CogsService:
    __LIB = pathlib.Path(__file__).parent.parent / "extensions"
    __EXTENSIONS: dict[str, Extension]

    __EXTENSION_ENABLED_ATTR = "is_enabled"

    __logger: Logger

    def __init__(self, bot: commands.Bot) -> None:
        self.__bot = bot
        self.__logger = loggers.logger(__name__)

        self.__EXTENSIONS = {
            mod.stem: Extension(
                name=mod.stem, description="", module=f"src.extensions.{mod.stem}"
            )
            for mod in self.__LIB.glob("*.py")
        }

    async def setup(self) -> None:
        if not self.are_all_extensions_loaded():
            self.__logger.info("Loading all extensions.")
            await self.load_all_extensions()

        if self.are_all_extensions_loaded():
            self.__logger.info("All extensions were successfully loaded.")

    def is_extension_loaded(self, extension: str) -> bool:
        """Check if an extension is loaded.

        Args:
            extension (str): The extension string import path

        Returns:
            bool: True if it is loaded.
        """

        if (ext := self.__EXTENSIONS.get(extension)) is None:
            raise ValueError("no extension were found in the extension map")

        return getattr(ext, self.__EXTENSION_ENABLED_ATTR, False)

    def are_all_extensions_loaded(self) -> bool:
        """This method returns true when all extensions are loaded.

        Returns:
            bool: True when all extensions are loaded, False otherwise.
        """

        return all(
            [self.is_extension_loaded(ext) for ext in self.__EXTENSIONS] or [False]
        )

    async def load_extension(self, extension: str) -> None:
        """This method loads an extension given by their path.

        Args:
            extension (str): The extension path.

        Raises:
            ValueError: When the extension is already loaded.
        """

        if (ext := self.__EXTENSIONS.get(extension)) is None:
            raise ValueError("no extension were found with the given name")

        setattr(ext, self.__EXTENSION_ENABLED_ATTR, True)

        await self.__bot.load_extension(ext.module)

    async def load_all_extensions(self) -> None:
        """This method loads all the existing extensions in the extensions path.

        Raises:
            ValueError: When some extension is already loaded.
        """
        for ext in self.__EXTENSIONS.values():
            await self.load_extension(ext.name)

    async def unload_extension(self, extension: str) -> None:
        """This method unload an extension given by their path.

        Args:
            extension (str): The extension path.

        Raises:
            ValueError: When the extension is already unloaded.
        """

        if (ext := self.__EXTENSIONS.get(extension)) is None:
            raise ValueError("no extension were found with the given name")

        setattr(ext, self.__EXTENSION_ENABLED_ATTR, False)

        await self.__bot.unload_extension(ext.module)

    async def unload_all_extension(self) -> None:
        """This method unloads all the existing extensions in the extension path.

        Raises:
            ValueError: When some extension is already unloaded.
        """
        for ext in self.__EXTENSIONS.values():
            await self.load_extension(ext.name)

    def get_enabled_extensions(self) -> list[Extension]:
        return [
            ext
            for ext in self.__EXTENSIONS.values()
            if self.is_extension_loaded(ext.name)
        ]

    def get_disabled_extensions(self) -> list[Extension]:
        return [
            ext
            for ext in self.__EXTENSIONS.values()
            if not self.is_extension_loaded(ext.name)
        ]
