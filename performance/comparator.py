from collections import Counter

from typing import List, Callable, Any, Sequence
from performance_types import Comparator, Printer, Measurement, TimedArgument
from printer import PerformancePrinter
from measurement import PerformanceMeasurement
from argument import RegularTimedArgument, VacuousTimedArgument


class PerformanceComparator(Comparator):
    """class measuring time elapsed during execution of functions.
    it compares several functions executing several arguments (one at a time) given number of times.

    results are printed in a table, each row being the execution time and percent describing how much longer
    the execution took compared with the shortest time.
    columns correspond to functions; the column name is taken from the documentation string of a function if present,
    otherwise it's just the function name.
    rows correspond to arguments; to customise the name of the row and argument can be passed as an instance of a class
    with fields 'description' and 'value'."""

    def __init__(self, functions: Sequence[Callable], arguments: Sequence[Any] = (), count: int = 1000) -> None:

        self.__funcs: Sequence[Callable] = functions
        self.__args: Sequence[TimedArgument] = self.__wrap_arguments(arguments)
        self.__count: int = count

        self.__measurements: Sequence[Measurement] = self.__measure_arguments()
        self.__sort_measured_functions()

        self.__printer: Printer = PerformancePrinter()

    def __wrap_arguments(self, arguments: Sequence[Any]) -> List[TimedArgument]:
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
        sorted_function_indices: Sequence[List[int]] = self.__get_function_indices_sorted_by_timings()

        return self.__produce_ordering_by_the_number_of_fastest_results(sorted_function_indices)

    def __get_function_indices_sorted_by_timings(self) -> Sequence[List[int]]:
        return [measurement.get_indices_sorted_by_timings() for measurement in self.__measurements]

    def __produce_ordering_by_the_number_of_fastest_results(self, sorted_indices: Sequence[List[int]]) -> List[int]:
        resultant_ordering: List[int] = []
        for n in range(len(self.__funcs)):
            most_common: int = self.__get_index_of_fastest_function(sorted_indices)
            resultant_ordering.append(most_common)
            sorted_indices: Sequence[List[int]] = self.__remove_index_of_fastest_function(most_common, sorted_indices)

        return resultant_ordering

    @staticmethod
    def __get_index_of_fastest_function(sorted_indices: Sequence[List[int]]) -> int:
        return Counter([indices[0] for indices in sorted_indices]).most_common(1)[0][0]

    @staticmethod
    def __remove_index_of_fastest_function(index: int, sorted_indices: Sequence[List[int]]) -> Sequence[List[int]]:
        for indices in sorted_indices:
            indices.remove(index)
        return sorted_indices

    def __sort_using_ordering(self, ordering: Sequence[int]):
        for measurement in self.__measurements:
            measurement.sort(ordering)

    def print(self) -> None:
        header_length: int = self.__printer.print_header(self.__funcs, self.__args)
        self.__printer.print_measurements_row(self.__measurements, header_length)


if __name__ == '__main__':

    # functions to be measured
    def function_one(value):
        return value**2/13

    def function_two(value):
        """described function"""
        return 156*(value % 12)

    # argument with custom description
    class TwentyFive:
        description = "described 25"
        value = 25

    # comparison of two functions with two arguments each
    PerformanceComparator([function_one, function_two], (12, TwentyFive())).print()

    print()

    # comparison of two functions without an argument
    PerformanceComparator([lambda: function_one(10), lambda: function_two(7)]).print()
