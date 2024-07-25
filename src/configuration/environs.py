import os


def get_environs(key: str) -> str:
    """Get a environ by giving a key

    Args:
        key (str): The environ key

    Raises:
        ValueError: When the key argument were empty
        RuntimeError: When no environ value were returned

    Returns:
        str: The environ value
    """

    if key == "" or key == None:
        raise ValueError("cannot use an empty string here")

    env = os.environ.get(key)

    if env == None:
        raise RuntimeError(f"there is no a environ variable with the key {key}")

    return env


def get_bool_environs(key: str) -> bool:
    """Get a boolean environment variable by giving a key

    Args:
        key (str): The environ key

    Raises:
        ValueError: When the key argument were empty
        RuntimeError: When no environ value were returned

    Returns:
        bool: The environ value as a boolean
    """

    if key == "" or key == None:
        raise ValueError("cannot use an emprty string here")

    env = os.environ.get(key)

    if env == None:
        raise RuntimeError(f"there is no a environ variable with the ke {key}")

    return bool(env)
