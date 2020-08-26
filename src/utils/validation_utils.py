from typing import List

from src.exceptions.attribute_not_found import AttributeNotFound
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


def require_list(obj: list):
    if not isinstance(obj, list):
        raise NotAListError


def require_email(email: str, obj: dict):
    pass
