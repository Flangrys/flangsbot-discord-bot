import logging


class CustomFormatter(logging.Formatter):

    __formats: dict[int, str] = {
        logging.NOTSET: "[%(asctime)s] \x1b[49m [%(levelname)s] \x1b[0m [%(name)s]: %(message)s",
        logging.DEBUG: "[%(asctime)s] \x1b[1,49m [%(levelname)s] \x1b[0m [%(name)s]: %(message)s",
        logging.INFO: "[%(asctime)s] \x1b[49m  [%(levelname)s] \x1b[0m [%(name)s]: %(message)s",
        logging.WARN: "[%(asctime)s] \x1b[49m [%(levelname)s] \x1b[0m [%(name)s]: %(message)s",
        logging.ERROR: "[%(asctime)s] \x1b[49m [%(levelname)s] \x1b[0m [%(name)s]: %(message)s",
        logging.CRITICAL: "[%(asctime)s] \x1b[49m [%(levelname)s] \x1b[0m [%(name)s]: %(message)s",
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
