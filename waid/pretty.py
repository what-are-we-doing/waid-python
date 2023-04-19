"""
Pretty-printing routines.
"""

import numbers


def elapsed_short(secs: numbers.Real) -> str:
    """
    Return a short, human-friendly representation of an elapsed time in seconds.
    Examples:

    * 293ms
    * 3.42s
    * 1m3.24s
    * 6h32m5s

    Args:
        secs(float):
            The elapsed time in seconds.
    """
    if secs < 1:
        return "{: 0.0f}ms".format(secs * 1000)
    elif secs > 60:
        m, s = divmod(secs, 60)
        if m > 60:
            h, m = divmod(m, 60)
            return "{:0.0f}h{:0.0f}m{:0.1d}s".format(h, m, s)
        else:
            return "{:0.0f}m{:0.2f}s".format(m, s)
    else:
        return "{:0.2f}s".format(secs)
