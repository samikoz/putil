import time
import functools
import itertools


class Timings:
    """only single-positional-argument functions are supported.
    if need be for more arguments, use functools.partial."""

    # think a little about the width with time as well
    # sorting logic
    # labelling arguments

    def __init__(self, functions, count=1000, arguments=()):
        self.__funcs = functions
        self.__args = [TimingArgument(arg) for arg in arguments] if arguments else [TimingArgument()]
        self.__count = count

        self.__measurements = [self.__measure_arg(argument) for argument in self.__args]

    def __measure_arg(self, argument):
        return Measurement(self.__funcs, self.__count, argument)

    def print(self):
        row_length = self.__print_header()
        for measurement in self.__measurements:
            measurement.print()
            print(' ' + '-' * (row_length-1))

    def __print_header(self):
        header = functools.reduce(lambda s, f: s + f' {self.__get_function_description(f)} |', self.__funcs, '')
        header_length = len(header)
        print(header)
        print(' ' + '-' * (header_length-1))
        return header_length

    @staticmethod
    def __get_function_description(f):
        return f.__doc__ or f.__name__


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

        return elapsed

    @staticmethod
    def __compute_ratios(timing_results):
        least_result = min(timing_results)
        return [result/least_result*100 - 100 for result in timing_results]

    def print(self):
        for result in self.__results:
            print(self.__format_single_measurement(result), end='')
        print()

        for ratio in self.__percent_ratios:
            print(self.__format_single_ratio(ratio), end='')
        self.__arg.print()

    @staticmethod
    def __format_single_measurement(elapsed):
        return f' {elapsed:12e} |'

    @staticmethod
    def __format_single_ratio(ratio):
        if abs(ratio) > 1e-5:
            return f' {ratio:+11.2f}% |'
        else:
            return ' ' * 12 + '- |'


class TimingArgument:
    class Empty:
        """marker class"""
        pass

    def __init__(self, arg=Empty()):
        self.__value = arg

    def apply_timed(self, f):
        if isinstance(self.__value, TimingArgument.Empty):
            start = time.time()
            f()
            end = time.time()
        else:
            start = time.time()
            f(self.__value)
            end = time.time()
        return end - start

    def print(self):
        if isinstance(self.__value, TimingArgument.Empty):
            print()
        else:
            print(f' {self.__value}')


if __name__ == '__main__':
    def function_one(value):
        return value**2/13

    def described_function(value):
        """function_two"""
        return 156*(value % 12)

    Timings([function_one, described_function], 1000, (12, 25)).print()
