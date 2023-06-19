from typing import TypeVar

_T = TypeVar("_T")


def deduplicate_list(data: list[_T]) -> list[_T]:
    return list(dict.fromkeys(data).keys())
