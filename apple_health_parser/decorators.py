import time
from functools import wraps

from apple_health_parser.utils.logging import logger


def timeit(func):
    """
    Decorator that logs how long a function takes to run.

    Wraps a function and logs its execution time in seconds using logger.info.

    Args:
        func: The function to wrap.

    Returns:
        The wrapped function that logs execution time.

    Example:
        @timeit
        def slow_function():
            time.sleep(1)
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        logger.info(f"Took {time.time() - start:.2f} seconds to run {func.__name__}")
        return result

    return wrapper
