import logging


class CustomFormatter(logging.Formatter):

    __formats: dict[int, str] = {
        logging.NOTSET: "\N{ESC}[30;40m[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s[0m",
        logging.DEBUG: "\N{ESC}[32;40m[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s[0m",
        logging.INFO: "\N{ESC}[34;40m[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s[0m",
        logging.WARN: "\N{ESC}[33;40m[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s[0m",
        logging.ERROR: "\N{ESC}[31;40m[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s[0m",
        logging.CRITICAL: "\N{ESC}[1m[31;40m[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s[0m",
    }

    def format(self, record: logging.LogRecord) -> str:
        fmt = self.__formats[record.levelno]
        return logging.Formatter(fmt=fmt).format(record=record)


def logger(name: str) -> logging.Logger:
    """Return a logger with the given name.

    Args:
        name (str): The logger name.

    Returns:
        logging.Logger: A logger with the given name.
    """
    formtr = CustomFormatter()

    handlr = logging.StreamHandler()
    handlr.setFormatter(fmt=formtr)

    logger = logging.getLogger(name)
    logger.addHandler(handlr)
    return logger
