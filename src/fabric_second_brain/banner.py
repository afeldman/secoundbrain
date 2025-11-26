"""Banner display utilities for the CLI."""

from art import text2art
from termcolor import colored


def print_banner() -> None:
    """Print a colorized ASCII art banner for 'Second Brain'.

    Uses the 'small' font from art library and displays in magenta.
    """
    banner = text2art("Second Brain", font="small")
    print(colored(banner, "magenta"))
