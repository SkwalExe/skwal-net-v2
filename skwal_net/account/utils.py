import re


def is_valid_username(username):
    return len(username) <= 32 and re.match(r"^[a-zA-Z0-9_\-\.]+$", username) and re.search(r"[a-zA-Z0-9]+", username)
