from pathlib import Path
from typing import List

from client import Flangsbot


class ExtensionsManager:

    EXTENSIONS_PATH: Path = Path(__file__).joinpath("extensions")
    EXTENSION_MODULES: List[str] = [
        path.stem for path in Path(EXTENSIONS_PATH).glob("*.py")
    ]

    def __init__(self, bot: "Flangsbot") -> None:
        self.bot = bot

    @staticmethod
    def is_extension_loaded(extension: str) -> bool:
        """Check if an extension is loaded.

        Args:
            extension (str): The extension string import path

        Raises:
            ValueError: When no extension exist with the given path

        Returns:
            bool: True if it is loaded.
        """
        if extension not in ExtensionsManager.EXTENSION_MODULES:
            raise ValueError(
                f"there is no a extension {extension} in the cogs directory"
            )

        return getattr(ExtensionsManager, extension)

    @staticmethod
    def is_all_extensions_loaded() -> bool:

        enabled_extensions_map = map(
            lambda ext: getattr(ExtensionsManager, ext),
            ExtensionsManager.EXTENSION_MODULES,
        )

        return all(enabled_extensions_map)

    async def load_extension(self, extension: str) -> None:
        if self.is_extension_loaded(extension):
            raise ValueError(f"the extension {extension} is already loaded")

        await self.bot.load_extension(extension)

    async def load_all_extensions(self) -> None:
        if self.is_all_extensions_loaded():
            raise ValueError("cannot load all the extensions that it is already loaded")

        map(self.load_extension, self.EXTENSION_MODULES)

    async def unload_extension(self, extension: str) -> None:
        if not self.is_extension_loaded(extension):
            raise ValueError(f"the extension {extension} is already loaded")

        await self.bot.unload_extension(extension, package=__package__)

    async def unload_all_extension(self) -> None:
        if not self.is_all_extensions_loaded():
            raise ValueError(
                "cannot unload all the extensions that it is already unloaded"
            )

        map(self.unload_extension, self.EXTENSION_MODULES)
