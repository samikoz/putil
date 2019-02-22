import time
import itertools
import functools
import operator


class Timings:
    # TODO implement labelling logic with manupulating docs
    # init will have to get the length of the first column
    # think a little about the width with time as well
    # and diffs n ratios to the top
    # allow for arguments - then more advanced sorting logic

    def __init__(self, funcs, count):
        self.__funcs_with_times = sorted(
            [(f, self.__measure_single(f, count)) for f in funcs],
            key=lambda f_t: f_t[1]
        )

    @staticmethod
    def __measure_single(func, count):
        start = time.time()
        for _ in itertools.repeat(None, count):
            func()
        end = time.time()

        return end - start

    @staticmethod
    def __format_single_measurement(elapsed):
        return f' | {elapsed:12e}'

    def __format_header(self):
        return functools.reduce(
            operator.add,
            map(lambda x: f' | {x[0].__doc__:12}', self.__funcs_with_times)
        ) + ' |'

    def print(self):
        print(self.__format_header())

        for _, t in self.__funcs_with_times:
            print(self.__format_single_measurement(t), end='')

        print(' |')
