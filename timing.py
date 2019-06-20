import abc
import time
import functools
import itertools
from collections import Counter


class Timings:
    """only single-positional-argument functions are supported.
    if need be for more arguments, use functools.partial.

    sorting in a simple manner: first function that is fastest in most cases, then fastest excluding the first etc."""

    def __init__(self, functions, count=1000, arguments=()):
        self.__column_width = 20
        self.__column_width += self.__column_width % 4  # make sure divisible by 4

        self.__funcs = functions
        self.__args = [RegularTimingArgument(arg) for arg in arguments] if arguments else [VacuousTimingArgument()]
        self.__count = count

        self.__measurements = [self.__measure_argument(argument) for argument in self.__args]
        self.__sort_within_measurements(self.__measurements)

    def __measure_argument(self, argument):
        return Measurement(self.__funcs, self.__count, argument)

    def __sort_within_measurements(self, measurements):
        sorted_indices = [measurement.get_indices_in_sorted_order() for measurement in measurements]

        resultant = []
        for n in range(len(self.__funcs)):
            most_common = Counter([indices[0] for indices in sorted_indices]).most_common(1)[0][0]
            resultant.append(most_common)
            for indices in sorted_indices:
                indices.remove(most_common)

        for measurement in measurements:
            measurement.sort_with_order(resultant)

    def print(self):
        row_length = self.__print_header()
        for measurement in self.__measurements:
            measurement.print(self.__column_width)
            print(' ' + '-' * (row_length-1))

    def __print_header(self):
        header = functools.reduce(lambda s, f: s + (' {0:^' + str(self.__column_width) + '} |').format(self.__get_function_description(f)), self.__funcs, '')
        header_length = len(header)
        print(header, end='')
        header_length += self.__args[0].print_header()
        print(' ' + '-' * (header_length-1))
        return header_length

    def __get_function_description(self, f):
        return f.__doc__[:self.__column_width] if f.__doc__ else f.__name__[:self.__column_width]


class Measurement:
    def __init__(self, functions, count, argument):
        self.__funcs = functions
        self.__count = count
        self.__arg = argument

        self.__results = [self.__measure_single(f) for f in functions]
        self.__percent_ratios = self.__compute_ratios(self.__results)

    def __measure_single(self, f):
        elapsed = 0
        for _ in itertools.repeat(None, self.__count):
            elapsed += self.__arg.apply_timed(f)

        return elapsed/self.__count

    @staticmethod
    def __compute_ratios(timing_results):
        least_result = min(timing_results)
        return [result/least_result*100 - 100 for result in timing_results]

    def get_indices_in_sorted_order(self):
        return list(map(
            lambda index_with_result: index_with_result[0],
            sorted(enumerate(self.__results), key=lambda x: x[1])
        ))

    def sort_with_order(self, order):
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


class TimingArgument(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def apply_timed(self, f):
        pass

    @abc.abstractmethod
    def print(self):
        pass

    @abc.abstractmethod
    def print_header(self):
        pass


class RegularTimingArgument(TimingArgument):
    def __init__(self, arg):
        self.__value = arg

    def apply_timed(self, f):
        start = time.time()
        f(self.__value.value if hasattr(self.__value, 'value') else self.__value)
        end = time.time()
        return end - start

    def print(self):
        if hasattr(self.__value, 'description'):
            print(f'| {self.__value.description[:9]:>9} |')
        else:
            print(f'| {str(self.__value)[:9]:>9} |')

    def print_header(self):
        print('| arguments |')
        return 13


class VacuousTimingArgument(TimingArgument):
    def apply_timed(self, f):
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

    Timings([function_one, described_function], 1000, (12, TwentyFive())).print()

    print()

    Timings([lambda: function_one(10), lambda: described_function(7)]).print()
