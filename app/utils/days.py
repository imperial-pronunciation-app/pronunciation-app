from datetime import datetime


def days_until_next_sunday() -> int:
    today = datetime.today().weekday()  # Monday = 0, Sunday = 6
    days_until_sunday = (6 - today) % 7  # If today is Sunday, returns 0
    return days_until_sunday if days_until_sunday else 7  # Ensures next Sunday is returned
