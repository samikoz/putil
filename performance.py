import abc
import time
import functools
import itertools
from collections import Counter


class PerformanceComparator:
    """only single-positional-argument functions are supported.
    if need be for more arguments, use functools.partial.
    arguments can be instances with fields 'value' and 'description'

    sorting in a simple manner: first function that is fastest in most cases, then fastest excluding the first etc."""

    column_width = 20

    def __init__(self, functions, count=1000, arguments=()):
        self.column_width += self.column_width % 4  # make sure divisible by 4

        self.__funcs = functions
        self.__args = [self.__wrap_argument(arg) for arg in arguments] if arguments else [VacuousTimedArgument()]
        self.__count = count

        self.__measurements = [self.__measure_argument(argument) for argument in self.__args]
        self.__sort_measurements()

    @staticmethod
    def __wrap_argument(argument):
        if hasattr(argument, 'value') and hasattr(argument, 'description'):
            return RegularTimedArgument(argument.value, argument.description)
        else:
            return RegularTimedArgument(argument)

    def __measure_argument(self, argument):
        return PerformanceMeasurement(self.__funcs, self.__count, argument)

    def __sort_measurements(self):
        ordering = self.__produce_final_ordering()
        self.__sort_using_ordering(ordering)

    def __produce_final_ordering(self):
        sorted_indices = [measurement.get_indices_sorted_by_timings() for measurement in self.__measurements]

        resultant = []
        for n in range(len(self.__funcs)):
            most_common = Counter([indices[0] for indices in sorted_indices]).most_common(1)[0][0]
            resultant.append(most_common)
            for indices in sorted_indices:
                indices.remove(most_common)

        return resultant

    def __sort_using_ordering(self, ordering):
        for measurement in self.__measurements:
            measurement.sort(ordering)

    def print(self):
        row_length = self.__print_header()
        for measurement in self.__measurements:
            measurement.print(self.column_width)
            print(' ' + '-' * (row_length-1))

    def __print_header(self):
        header = functools.reduce(lambda s, f: s + (' {0:^' + str(self.column_width) + '} |').format(self.__get_function_description(f)), self.__funcs, '')
        header_length = len(header)
        print(header, end='')
        header_length += self.__args[0].print_header()
        print(' ' + '-' * (header_length-1))
        return header_length

    def __get_function_description(self, f):
        return f.__doc__[:self.column_width] if f.__doc__ else f.__name__[:self.column_width]


class PerformanceMeasurement:
    def __init__(self, functions, count, argument):
        self.__funcs = functions
        self.__count = count
        self.__arg = argument

        self.__results = [self.__measure_single(f) for f in functions]
        self.__percent_ratios = self.__compute_ratios(self.__results)

    def __measure_single(self, f):
        elapsed = 0
        for _ in itertools.repeat(None, self.__count):
            elapsed += self.__arg.apply(f)

        return elapsed/self.__count

    @staticmethod
    def __compute_ratios(timing_results):
        least_result = min(timing_results)
        return [result/least_result*100 - 100 for result in timing_results]

    def get_indices_sorted_by_timings(self):
        return list(map(
            lambda index_with_result: index_with_result[0],
            sorted(enumerate(self.__results), key=lambda x: x[1])
        ))

    def sort(self, order):
        self.__results = [self.__results[i] for i in order]
        self.__percent_ratios = [self.__percent_ratios[i] for i in order]

    def print(self, width):
        for result, ratio in zip(self.__results, self.__percent_ratios):
            print(self.__format_single_measurement(result, width), end='')
            print(self.__format_single_ratio(ratio, width), end='')
        self.__arg.print()

    @staticmethod
    def __format_single_measurement(elapsed, width):
        return (' {0:<' + str((width//2)-1) + '.2e} ').format(elapsed)

    @staticmethod
    def __format_single_ratio(ratio, width):
        if abs(ratio) > 1e-5:
            return (' {0:+' + str((width//2)-2) + '.2f}% |').format(ratio)
        else:
            return ' ' * (width//4) + '-' + ' ' * (width//4) + '|'


class TimedArgument(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def apply(self, f):
        pass

    @abc.abstractmethod
    def print(self):
        pass

    @abc.abstractmethod
    def print_header(self):
        pass


class RegularTimedArgument(TimedArgument):
    def __init__(self, argument, description=None):
        self.value = argument
        self.description = description or str(argument)

    def apply(self, f):
        start = time.time()
        f(self.value)
        end = time.time()
        return end - start

    def print(self):
        print(f'| {self.description[:9]:>9} |')

    def print_header(self):
        print('| arguments |')
        return 13


class VacuousTimedArgument(TimedArgument):
    def apply(self, f):
        start = time.time()
        f()
        end = time.time()
        return end - start

    def print(self):
        print()

    def print_header(self):
        print()
        return 0


if __name__ == '__main__':
    def function_one(value):
        return value**2/13

    def described_function(value):
        """function_two_two_two_twentytwo"""
        return 156*(value % 12)

    class TwentyFive:
        description = "twentyfive-twentyfive"
        value = 25

    PerformanceComparator([function_one, described_function], 1000, (12, TwentyFive())).print()

    print()

    PerformanceComparator([lambda: function_one(10), lambda: described_function(7)]).print()
