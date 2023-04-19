"""
Support for reporting timing data.
"""

import time

from . import pretty


class Stopwatch():
    """
    Timer class for recording elapsed wall time in operations.  Time is measured
    using :func:`time.perf_counter`.

    Its string representation is provided by :meth:`pretty_elapsed`.
    """
    start_time = None
    stop_time = None

    def __init__(self, start: bool=True):
        if start:
            self.start()

    def start(self):
        """
        Start the timer.  If the timer is already started, *restarts* the timer.
        """
        self.start_time = time.perf_counter()

    def stop(self):
        """
        Stop the timer, recording the current time.
        """
        self.stop_time = time.perf_counter()

    def elapsed(self) -> float:
        """
        Return the elapsed time, in seconds.  If the timer is still running, this is
        the time between the start and now; if it has been stopped, it is the time
        between start and stop.
        """

        stop = self.stop_time
        if stop is None:
            stop = time.perf_counter()

        return stop - self.start_time

    def pretty_elapsed(self):
        """
        Return a short pretty-printed version of the elapsed time, formatted with
        :func:`~waid.pretty.elapsed_short`.
        """
        return pretty.elapsed_short(self.elapsed())

    def __str__(self):
        return self.pretty_elapsed()
