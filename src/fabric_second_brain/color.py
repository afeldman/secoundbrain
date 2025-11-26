"""Color utilities for terminal output."""

from termcolor import colored


def info(msg: str) -> str:
    """Return cyan-colored text for informational messages.

    Args:
        msg: The message string to colorize.

    Returns:
        Colorized string in cyan.
    """
    return colored(msg, "cyan")


def success(msg: str) -> str:
    """Return green-colored text for success messages.

    Args:
        msg: The message string to colorize.

    Returns:
        Colorized string in green.
    """
    return colored(msg, "green")


def warn(msg: str) -> str:
    """Return yellow-colored text for warning messages.

    Args:
        msg: The message string to colorize.

    Returns:
        Colorized string in yellow.
    """
    return colored(msg, "yellow")


def error(msg: str) -> str:
    """Return red-colored text for error messages.

    Args:
        msg: The message string to colorize.

    Returns:
        Colorized string in red.
    """
    return colored(msg, "red")


def magenta(msg: str) -> str:
    """Return magenta-colored text.

    Args:
        msg: The message string to colorize.

    Returns:
        Colorized string in magenta.
    """
    return colored(msg, "magenta")
