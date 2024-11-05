import os
from datetime import datetime


def get_date_month_year(user_date):
    date_obj = datetime.strptime(user_date, "%Y-%m-%d")
    day = int(date_obj.strftime("%d"))  # Convert day to an integer to remove leading zeros
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]

    day_ordinal = str(day) + suffix
    return day_ordinal, date_obj.strftime("%B"), date_obj.strftime("%Y")


def convert_date_string(date_string):
    try:
        date_obj = datetime.strptime(date_string, "%b-%Y")
        formatted_date = date_obj.strftime("%B %Y")
        return formatted_date
    except ValueError:
        return None  # Handle invalid date strings gracefully


def split_string(name, max_length):
    if len(name) <= max_length:
        return name, ""
    else:
        last_space_index = name[:max_length].rfind(' ')
        if last_space_index != -1:
            return name[:last_space_index], name[last_space_index + 1:]
        else:
            return name[:max_length], name[max_length:]


def check_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)
