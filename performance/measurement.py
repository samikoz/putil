import itertools

from performance_types import Measurement, Printer
from typing import Callable, List, Any


class PerformanceMeasurement(Measurement):
    def __init__(self, functions: List[Callable], argument: Any, count: int) -> None:
        self.__funcs: List[Callable] = functions
        self.__count: int = count
        self.__arg: Any = argument

        self.__results: List[float] = self.__do_measurements()
        self.__percent_ratios: List[float] = self.__compute_ratios_to_the_fastest()

    def __do_measurements(self) -> List[float]:
        return [self.__measure_single(f) for f in self.__funcs]

    def __measure_single(self, f: Callable) -> float:
        elapsed: int = 0
        for _ in itertools.repeat(None, self.__count):
            elapsed += self.__arg.apply(f)

        return elapsed/self.__count

    def __compute_ratios_to_the_fastest(self) -> List[float]:
        least_result: float = min(self.__results)
        return [result/least_result*100 - 100 for result in self.__results]

    def get_indices_sorted_by_timings(self) -> List[int]:
        return list(map(
            lambda index_with_result: index_with_result[0],
            sorted(enumerate(self.__results), key=lambda x: x[1])
        ))

    def sort(self, order: List[int]) -> None:
        self.__results: List[float] = [self.__results[i] for i in order]
        self.__percent_ratios: List[float] = [self.__percent_ratios[i] for i in order]

    def print(self, printer: Printer) -> None:
        for result, ratio in zip(self.__results, self.__percent_ratios):
            self.__print_single_result_with_ratio(printer, result, ratio)
        self.__print_argument_name()

    @staticmethod
    def __print_single_result_with_ratio(printer: Printer, result: float, ratio: float):
        print(printer.get_single_measurement_format().format(result), end='')
        if abs(ratio) > 1e-5:
            print(printer.get_nontrivial_ratio_format().format(ratio), end='')
        else:
            print(printer.get_trivial_ratio_format().format(ratio), end='')

    def __print_argument_name(self) -> None:
        self.__arg.print()
