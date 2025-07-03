from abc import ABC, abstractmethod
from typing import Any, Optional, Tuple


class Validator(ABC):
    protected_name: Optional[str] = None

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance: Any, owner: type) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: Any) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value: int = min_value
        self.max_value: int = max_value

    def validate(self, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"Quantity should not be less than {self.min_value} and "
                f"greater than {self.max_value}."
            )


class OneOf(Validator):
    def __init__(self, options: Tuple[str, ...]) -> None:
        self.options: Tuple[str, ...] = options

    def validate(self, value: Any) -> None:
        if value not in self.options:
            raise ValueError(
                f"Expected {value} to be one of {self.options}."
            )


class BurgerRecipe:
    buns: Number = Number(min_value=2, max_value=3)
    cheese: Number = Number(min_value=0, max_value=2)
    tomatoes: Number = Number(min_value=0, max_value=3)
    cutlets: Number = Number(min_value=1, max_value=3)
    eggs: Number = Number(min_value=0, max_value=2)
    sauce: OneOf = OneOf(options=("ketchup", "mayo", "burger"))

    def __init__(
        self,
        buns: int,
        cheese: int,
        tomatoes: int,
        cutlets: int,
        eggs: int,
        sauce: str
    ) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
