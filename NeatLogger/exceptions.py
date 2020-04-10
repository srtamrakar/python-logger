from typing import Any, NoReturn


class InvalidValue(Exception):
    def __init__(self, value: Any, allowed_value_list: list) -> NoReturn:
        self.value = value
        self.allowed_value_list = allowed_value_list

    def __str__(self) -> str:
        return f"'{self.value}' is not one of the allowed values: {self.allowed_value_list}."
