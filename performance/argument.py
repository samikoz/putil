import time

from performance_types import TimedArgument
from typing import Callable, Any


class RegularTimedArgument(TimedArgument):
    def __init__(self, argument: Any, description: str = None) -> None:
        self.value: Any = argument
        self.description: str = description or str(argument)

    def apply(self, f: Callable) -> float:
        start: float = time.time()
        f(self.value)
        end: float = time.time()
        return end - start

    def print(self) -> None:
        print(f'| {self.description[:9]:>9} |')

    def print_header(self) -> int:
        print('| arguments |')
        return 13


class VacuousTimedArgument(TimedArgument):
    def apply(self, f: Callable) -> float:
        start: float = time.time()
        f()
        end: float = time.time()
        return end - start

    def print(self) -> None:
        print()

    def print_header(self) -> int:
        print()
        return 0
