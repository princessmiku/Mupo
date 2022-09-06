import os

from colorama import Fore


startup_text = """Welcome to the music suggestion thing!"""


def _createPrefix(text: str) -> str:
    return Fore.WHITE + "[" + Fore.CYAN + text + Fore.WHITE + "] " + Fore.RESET


prefix_loading = _createPrefix("LOADING")
prefix_select = _createPrefix("SELECT")
prefix_login = _createPrefix("LOGIN")


def clearing():
    os.system('cls' if os.name == 'nt' else 'clear')
