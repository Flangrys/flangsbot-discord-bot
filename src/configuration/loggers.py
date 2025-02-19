import logging


class CustomFormatter(logging.Formatter):
    WHITE = "\x1b[m"
    BLACK = "\x1b[30m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    BLUE = "\x1b[34m"
    PURPLE = "\x1b[35m"
    CYAN = "\x1b[36m"
    GRAY = "\x1b[37m"
    RESET = "\x1b[0m"

    time_format = "[%(asctime)s] "
    level_format = "[%(levelname)s] "
    name_format = " [%(name)s]"
    message_format = ": %(message)s"

    __formats = {
        logging.NOTSET: WHITE
                        + time_format
                        + "\x1b[30;47m "
                        + level_format
                        + RESET
                        + WHITE
                        + name_format
                        + message_format
                        + RESET,
        logging.DEBUG: WHITE
                       + time_format
                       + "\x1b[30;42m "
                       + level_format
                       + RESET
                       + WHITE
                       + name_format
                       + message_format
                       + RESET,
        logging.INFO: WHITE
                      + time_format
                      + "\x1b[1;44m "
                      + level_format
                      + RESET
                      + WHITE
                      + name_format
                      + message_format
                      + RESET,
        logging.WARNING: WHITE
                         + time_format
                         + "\x1b[30;43m "
                         + level_format
                         + RESET
                         + WHITE
                         + name_format
                         + message_format
                         + RESET,
        logging.ERROR: WHITE
                       + time_format
                       + "\x1b[1;41m "
                       + level_format
                       + RESET
                       + WHITE
                       + name_format
                       + message_format
                       + RESET,
        logging.CRITICAL: WHITE
                          + time_format
                          + "\x1b[1;45m "
                          + level_format
                          + RESET
                          + WHITE
                          + name_format
                          + message_format
                          + RESET,
    }

    def format(self, record: logging.LogRecord):
        fmt = self.__formats.get(record.levelno)
        formatter = logging.Formatter(fmt)
        return formatter.format(record)


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

    log = logging.getLogger(name)
    log.addHandler(handlr)
    return log
