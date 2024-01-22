import os
from functools import lru_cache

import requests
from dotenv import load_dotenv

load_dotenv()

session_cookie = os.getenv("SESSION_COOKIE")


@lru_cache
def get_input(
    year: int, day: int, session_cookie: str = session_cookie
) -> requests.Response.text:
    """Gets the input for a given year and day from the Advent of Code website.

    Args:
        session_cookie (str): Your Advent of Code session cookie.
        year (int): The year of the puzzle. Format: YYYY
        day (int): The day of the puzzle. Format: DD
    """
    response = requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input",
        cookies={"session": session_cookie},
    )
    return response.text
