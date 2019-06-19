import time
import functools
import itertools


class Timings:
    """only single-positional-argument functions are supported.
    if need be for more arguments, use functools.partial."""

    # sorting logic
    # restructure TimingArgument into itself and EmptyTimingArgument

    def __init__(self, functions, count=1000, arguments=()):
        self.__column_width = 20
        self.__column_width += self.__column_width % 4  # make sure divisible by 4

        self.__funcs = functions
        self.__args = [TimingArgument(arg) for arg in arguments] if arguments else [TimingArgument()]
        self.__count = count

        self.__measurements = [self.__measure_argument(argument) for argument in self.__args]

    def __measure_argument(self, argument):
        return Measurement(self.__funcs, self.__count, argument)

    def print(self):
        row_length = self.__print_header()
        for measurement in self.__measurements:
            measurement.print(self.__column_width)
            print(' ' + '-' * (row_length-1))

    def __print_header(self):
        header = functools.reduce(lambda s, f: s + (' {0:^' + str(self.__column_width) + '} |').format(self.__get_function_description(f)), self.__funcs, '')
        header_length = len(header)
        print(header, end='')
        print('| arguments |')
        header_length += 13
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


class TimingArgument:
    class Empty:
        description = ''

    def __init__(self, arg=Empty()):
        self.__value = arg

    def apply_timed(self, f):
        if isinstance(self.__value, TimingArgument.Empty):
            start = time.time()
            f()
            end = time.time()
        else:
            start = time.time()
            f(self.__value.value if hasattr(self.__value, 'value') else self.__value)
            end = time.time()
        return end - start

    def print(self):
        if hasattr(self.__value, 'description'):
            print(f'| {self.__value.description[:9]:>9} |')
        else:
            print(f'| {str(self.__value)[:9]:>9} |')


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

    Timings([lambda: function_one(10), lambda: described_function(7)]).print()
