from collections import Counter

from typing import List, Callable, Any
from performance_types import Comparator, Printer, Measurement, TimedArgument
from printer import PerformancePrinter
from measurement import PerformanceMeasurement
from argument import RegularTimedArgument, VacuousTimedArgument


class PerformanceComparator(Comparator):
    """only single-positional-argument functions are supported.
    if need be for more arguments, use functools.partial.
    arguments can be instances with fields 'value' and 'description'

    sorting in a simple manner: first function that is fastest in most cases, then fastest excluding the first etc."""

    def __init__(self, functions: List[Callable], arguments: List[Any] = (), count: int = 1000) -> None:

        self.__funcs: List[Callable] = functions
        self.__args: List[TimedArgument] = self.__wrap_arguments(arguments)
        self.__count: int = count

        self.__measurements: List[Measurement] = self.__measure_arguments()
        self.__sort_measured_functions()

        self.__printer: Printer = PerformancePrinter()

    def __wrap_arguments(self, arguments: List[Any]) -> List[TimedArgument]:
        return [self.__wrap_regular_argument(arg) for arg in arguments] if arguments else [VacuousTimedArgument()]

    @staticmethod
    def __wrap_regular_argument(argument: Any) -> TimedArgument:
        if hasattr(argument, 'value') and hasattr(argument, 'description'):
            return RegularTimedArgument(argument.value, argument.description)
        else:
            return RegularTimedArgument(argument)

    def __measure_arguments(self) -> List[Measurement]:
        return [PerformanceMeasurement(self.__funcs, argument, self.__count) for argument in self.__args]

    def __sort_measured_functions(self) -> None:
        ordering: List[int] = self.__produce_final_ordering()
        self.__sort_using_ordering(ordering)

    def __produce_final_ordering(self) -> List[int]:
        sorted_function_indices_within_measurements: List[List[int]] = self.__get_function_indices_sorted_by_timings()

        return self.__produce_ordering_by_the_number_of_fastest_results(sorted_function_indices_within_measurements)

    def __get_function_indices_sorted_by_timings(self) -> List[List[int]]:
        return [measurement.get_indices_sorted_by_timings() for measurement in self.__measurements]

    def __produce_ordering_by_the_number_of_fastest_results(self, sorted_indices: List[List[int]]) -> List[int]:
        resultant_ordering: List[int] = []
        for n in range(len(self.__funcs)):
            most_common: int = self.__get_index_of_fastest_function(sorted_indices)
            resultant_ordering.append(most_common)
            sorted_indices: List[List[int]] = self.__remove_index_of_fastest_function(most_common, sorted_indices)

        return resultant_ordering

    @staticmethod
    def __get_index_of_fastest_function(sorted_indices: List[List[int]]) -> int:
        return Counter([indices[0] for indices in sorted_indices]).most_common(1)[0][0]

    @staticmethod
    def __remove_index_of_fastest_function(index: int, sorted_indices: List[List[int]]) -> List[List[int]]:
        for indices in sorted_indices:
            indices.remove(index)
        return sorted_indices

    def __sort_using_ordering(self, ordering: List[int]):
        for measurement in self.__measurements:
            measurement.sort(ordering)

    def print(self) -> None:
        header_length: int = self.__printer.print_header(self.__funcs, self.__args)
        self.__printer.print_measurements_row(self.__measurements, header_length)


if __name__ == '__main__':
    def function_one(value):
        return value**2/13

    def described_function(value):
        """function_two_two_two_twentytwo"""
        return 156*(value % 12)

    class TwentyFive:
        description = "twentyfive-twentyfive"
        value = 25

    PerformanceComparator([function_one, described_function], (12, TwentyFive())).print()

    print()

    PerformanceComparator([lambda: function_one(10), lambda: described_function(7)]).print()
