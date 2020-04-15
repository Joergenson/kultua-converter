import functools

from flask import request


def url_from_body(func):
    @functools.wraps(func)
    def wrapper(*args, **__):
        url = request.json.get("url")
        return func(*args, url)

    return wrapper


def name_from_body(func):
    @functools.wraps(func)
    def wrapper(*args, **__):
        name = request.json.get("name")
        return func(*args, name)

    return wrapper