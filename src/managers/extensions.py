import pathlib
from typing import override

from discord.ext import commands

from src.managers import abc
from src.types import extension


class ExtensionsManager(abc.AbstractManager):

    EXTENSIONS_HASH: dict[str, int]
    EXTENSIONS_LIST: list[extension.Extension]
    EXTENSIONS_PATH: list[pathlib.Path]

    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(bot, service=None)

        self.EXTENSIONS_HASH = {}
        self.EXTENSIONS_LIST = []
        self.EXTENSIONS_PATH = [
            path for path in self.get_extensions_path().glob("*.py")
        ]

        for index in range(len(self.EXTENSIONS_PATH)):
            __extension_name = self.EXTENSIONS_PATH[index].stem
            __extension_package = self.EXTENSIONS_PATH[index].name
            __extension_enabled = False

            self.EXTENSIONS_HASH.update({__extension_name: index})
            self.EXTENSIONS_LIST.append(
                {
                    "name": __extension_name,
                    "package": __extension_package,
                    "enabled": __extension_enabled,
                }
            )

    @override
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

        index = self.EXTENSIONS_HASH[extension]
        return self.EXTENSIONS_LIST[index]["enabled"]

    def is_all_extensions_loaded(self) -> bool:
        """This method returns true when all of the extensions are loaded.

        Returns:
            bool: True when all extensions are loaded, False otherwise.
        """

        return all([ext["enabled"] for ext in self.EXTENSIONS_LIST] or [False])

    async def load_extension(self, extension: str) -> None:
        """This method loads an extension given by their path.

        Args:
            extension (str): The extension path.

        Raises:
            ValueError: When the extension is already loaded.
        """

        if extension not in self.EXTENSIONS_HASH:
            raise ValueError(
                f"the extension {extension} does not exist in the extensions path"
            )

        if self.is_extension_loaded(extension):
            raise ValueError(f"the extension {extension} is already loaded")

        __extension = self.EXTENSIONS_HASH[extension]
        self.EXTENSIONS_LIST[__extension]["enabled"] = True

        full_extension_name = "src.extensions." + extension

        await self.client.load_extension(full_extension_name)

    async def load_all_extensions(self) -> None:
        """This method loads all the existing extensions in the extensions path.

        Raises:
            ValueError: When some extension is already loaded.
        """

        if self.is_all_extensions_loaded():
            raise ValueError("cannot load all the extensions that it is already loaded")

        for extension in self.EXTENSIONS_HASH:
            await self.load_extension(extension)

    async def unload_extension(self, extension: str) -> None:
        """This method unload an extension given by their path.

        Args:
            extension (str): The extension path.

        Raises:
            ValueError: When the extension is already unloaded.
        """

        if extension not in self.EXTENSIONS_HASH:
            raise ValueError(
                f"the extension {extension} does not exist in the extensions path"
            )

        if not self.is_extension_loaded(extension):
            raise ValueError(f"the extension {extension} is already unloaded")

        __extension = self.EXTENSIONS_HASH[extension]
        self.EXTENSIONS_LIST[__extension]["enabled"] = False

        full_extension_name = "src.extensions." + extension

        await self.client.unload_extension(full_extension_name)

    async def unload_all_extension(self) -> None:
        """This method unloads all the existing extensions in the extension path.

        Raises:
            ValueError: When some extension is already unloaded.
        """
        if not self.is_all_extensions_loaded():
            raise ValueError(
                "cannot unload all the extensions that it is already unloaded"
            )

        for extension in self.EXTENSIONS_HASH:
            await self.unload_extension(extension)

    def get_enabled_extensions(self) -> list[str]:
        enabled_extensions: list[str] = []

        for ext in self.EXTENSIONS_LIST:
            if ext["enabled"]:
                enabled_extensions.append(ext["name"])

        return enabled_extensions
