import datetime
from pathlib import Path


def parse_date(date: str) -> datetime.date:
    """
    Parse date from a string.

    Args:
        date: A string of date.

    Returns:
        A datetime.date object.
    """
    if date == "today":
        return datetime.date.today()
    elif date == "yesterday":
        return datetime.date.today() - datetime.timedelta(days=1)
    else:
        return datetime.datetime.strptime(date, "%Y-%m-%d").date()


def parse_interests(interests: str) -> str:
    """
    Parse interests from a file or a string.

    Args:
        interests: Path to a file or a string of interests.

    Returns:
        A string of interests.
    """
    if Path(interests).exists():
        with open(interests, "r") as f:
            return f.read().replace("\n", "")
    else:
        return interests
