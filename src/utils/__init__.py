import time
from functools import wraps

from .encoder import DFDataEncoder
from .indexer import DataIndexer


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__name__} executed in {end - start:.6f} seconds")
        return result

    return wrapper


__all__ = ["timeit", "DFDataEncoder", "DataIndexer"]
