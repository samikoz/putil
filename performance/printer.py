import functools

from performance_types import Printer, Measurement
from typing import Callable, List, Any


class PerformancePrinter(Printer):
    column_width: int = 20

    def __init__(self) -> None:
        self.column_width += self.column_width % 4

    def print_header(self, functions: List[Callable], arguments: List[Any]) -> int:
        function_descriptions_length: int = self.__print_function_descriptions(functions)
        header_length: int = function_descriptions_length + self.__print_argument_header(arguments)
        self.__print_header_underline(header_length)
        return header_length

    def __print_function_descriptions(self, functions: List[Callable]) -> int:
        header: str = functools.reduce(
            lambda s, f: s + self.__get_formatted_function_description(f),
            functions,
            ''
        )
        print(header, end='')
        return len(header)

    def __get_formatted_function_description(self, function: Callable) -> str:
        return self.__get_function_description_format().format(self.__get_function_description(function))

    def __get_function_description_format(self) -> str:
        return ' {0:^' + str(self.column_width) + '} |'

    def __get_function_description(self, f: Callable) -> str:
        return f.__doc__[:self.column_width] if f.__doc__ else f.__name__[:self.column_width]

    @staticmethod
    def __print_argument_header(arguments: List[Any]) -> int:
        return arguments[0].print_header()

    @staticmethod
    def __print_header_underline(length: int) -> None:
        print(' ' + '-' * (length - 1))

    def print_measurements_row(self, measurements: List[Measurement], row_length: int) -> None:
        for measurement in measurements:
            measurement.print(self)
            print(' ' + '-' * (row_length-1))

    def get_single_measurement_format(self) -> str:
        return ' {0:<' + str((self.column_width//2)-2) + '.2e}s '

    def get_nontrivial_ratio_format(self) -> str:
        return ' {0:+' + str((self.column_width//2)-2) + '.2f}% |'

    def get_trivial_ratio_format(self) -> str:
        return ' ' * (self.column_width//4) + '-' + ' ' * (self.column_width//4) + '|'
