import logging


class CustomFormatter(logging.Formatter):

    __formats: dict[int, str] = {
        logging.NOTSET: "\n\x1b[30;40m [%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s \x1b[0m",
        logging.DEBUG: "\n\x1b[32;40m [%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s \x1b[0m",
        logging.INFO: "\n\x1b[34;40m [%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s \x1b[0m",
        logging.WARN: "\n\x1b[33;40m [%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s \x1b[0m",
        logging.ERROR: "\n\x1b[31;40m [%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s \x1b[0m",
        logging.CRITICAL: "\n\x1b[31;1m [%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s \x1b[0m",
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
