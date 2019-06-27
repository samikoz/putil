import functools

from performance_types import Printer


class PerformancePrinter(Printer):
    column_width = 20

    def __init__(self):
        self.column_width += self.column_width % 4

    def print_header(self, functions, arguments):
        function_descriptions_length = self.__print_function_descriptions(functions)
        header_length = function_descriptions_length + self.__print_argument_header(arguments)
        self.__print_header_underline(header_length)
        return header_length

    def __print_function_descriptions(self, functions):
        header = functools.reduce(
            lambda s, f: s + self.__get_formatted_function_description(f),
            functions,
            ''
        )
        print(header, end='')
        return len(header)

    def __get_formatted_function_description(self, function):
        return self.__get_function_description_format().format(self.__get_function_description(function))

    def __get_function_description_format(self):
        return ' {0:^' + str(self.column_width) + '} |'

    def __get_function_description(self, f):
        return f.__doc__[:self.column_width] if f.__doc__ else f.__name__[:self.column_width]

    @staticmethod
    def __print_argument_header(arguments):
        return arguments[0].print_header()

    @staticmethod
    def __print_header_underline(length):
        print(' ' + '-' * (length - 1))

    def print_measurements_row(self, measurements, row_length):
        for measurement in measurements:
            measurement.print(self)
            print(' ' + '-' * (row_length-1))

    def get_single_measurement_format(self):
        return ' {0:<' + str((self.column_width//2)-2) + '.2e}s '

    def get_nontrivial_ratio_format(self):
        return ' {0:+' + str((self.column_width//2)-2) + '.2f}% |'

    def get_trivial_ratio_format(self):
        return ' ' * (self.column_width//4) + '-' + ' ' * (self.column_width//4) + '|'
