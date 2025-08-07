from dataclasses import dataclass
from typing import Any, Iterator


@dataclass
class DataStream(Iterator[Any]):

    def __post_init__(self):
        """set self._iter"""
        ...

    def __iter__(self):
        return self

    def __type__(self):
        return self.__class__.__repr__

    def __next__(self): ...

    def __iter__(self):
        """returns an iterator over the data stream with [title/key, data]"""
        ...


class FileDataStream(DataStream):

    def __post_init__(self):
        """set self._iter"""
        ...


class APIDataStream(DataStream):

    def __post_init__(self):
        """set self._iter"""
        ...
