import asyncio

from src import client

__version__ = (0, 1, 0, "indev")

if __name__ == "__main__":

    __bot = client.Flangsbot(version=__version__)  # type: ignore

    try:
        asyncio.run(__bot.launcher())

    except KeyboardInterrupt:
        print("bye.")
