import abc

from typing import Callable, List, Any, Sequence


class TimedArgument(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def apply(self, f: Callable) -> float:
        pass

    @abc.abstractmethod
    def print(self) -> None:
        pass

    @abc.abstractmethod
    def print_header(self) -> int:
        pass


class Measurement(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_indices_sorted_by_timings(self) -> List[int]:
        pass

    @abc.abstractmethod
    def sort(self, order: Sequence[int]) -> None:
        pass

    @abc.abstractmethod
    def print(self, printer) -> None:
        pass


class Printer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def print_header(self, functions: Sequence[Callable], arguments: Sequence[Any]):
        pass

    @abc.abstractmethod
    def print_measurements_row(self, measurements: Sequence[Measurement], row_length) -> None:
        pass

    @abc.abstractmethod
    def get_single_measurement_format(self) -> str:
        pass

    @abc.abstractmethod
    def get_nontrivial_ratio_format(self) -> str:
        pass

    @abc.abstractmethod
    def get_trivial_ratio_format(self) -> str:
        pass


class Comparator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def print(self) -> None:
        pass
