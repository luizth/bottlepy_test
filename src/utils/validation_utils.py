from typing import List
import re

from src.exceptions.attribute_not_found import AttributeNotFound
from src.exceptions.invalid_email_address import InvalidEmailAddress
from src.exceptions.not_a_list import NotAListError


def require_attrs(names: List[str], obj: dict) -> None:
    for name in names:
        require_attr(name, obj)


def require_attr(name: str, obj: dict) -> None:
    if name not in obj:
        raise AttributeNotFound


def require_dict(obj: dict) -> None:
    if not isinstance(obj, dict):
        raise NotADirectoryError


def require_list(obj: list) -> None:
    if not isinstance(obj, list):
        raise NotAListError


def require_email(email: str) -> None:
    regex = '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

    if not re.search(regex, email):
        raise InvalidEmailAddress
