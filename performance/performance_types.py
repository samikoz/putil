import abc


class Comparator(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def print(self):
        pass


class Printer(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def print_header(self, functions, arguments):
        pass

    @abc.abstractmethod
    def print_measurements(self, measurements, row_length):
        pass

    @abc.abstractmethod
    def format_single_measurement(self):
        pass

    @abc.abstractmethod
    def format_nontrivial_ratio(self):
        pass

    @abc.abstractmethod
    def format_trivial_ratio(self):
        pass


class Measurement(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_indices_sorted_by_timings(self):
        pass

    @abc.abstractmethod
    def sort(self, order):
        pass

    @abc.abstractmethod
    def print(self, printer):
        pass


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
