import os


def get_environ(key: str) -> str:
    """Get an environ by giving a key

    Args:
        key (str): The environ variable key.

    Raises:
        ValueError: When the key argument were empty.
        RuntimeError: When no environ value were returned.

    Returns:
        str: The environ variable as an string.
    """

    if key == "" or key == None:
        raise ValueError("cannot use an empty string here")

    env = os.environ.get(key)

    if env == None:
        raise RuntimeError(f"there is no an environ variable with the key {key}")

    return env


def get_bool_environ(key: str) -> bool:
    """Get a boolean environment variable by giving a key.

    Args:
        key (str): The environ variable key.

    Raises:
        ValueError: When the key argument were empty.
        RuntimeError: When no environ value were returned.

    Returns:
        bool: The environ value as a boolean.
    """

    env = get_environ(key)

    return bool(env)


def get_integer_environ(key: str) -> int:
    """Get a integer environ variable given a key.

    Args:
        key (str): The environ variable key.

    Returns:
        int: The environ variable as an integer.
    """
    env = get_environ(key)

    return int(env)
