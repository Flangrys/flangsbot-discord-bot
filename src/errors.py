from discord.app_commands.errors import AppCommandError, CheckFailure


class NotAGuildException(CheckFailure):
    """
    An exception raised when a command is run outside a guild.
    """

    pass


class NotAChannelException(CheckFailure):
    """
    An exception raised when a channel does not exist or is missing.
    """

    pass


class NotAMemberException(CheckFailure):
    """
    An exception raised when a user is not a guild member.
    """

    pass


class TransferException(AppCommandError):
    """
    An exception raised when a user cannot be transferd or moved.
    """

    pass
