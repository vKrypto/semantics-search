import json
import logging  # type: ignore
import logging.config
import os


def setup_logger():
    filepath = os.path.join(os.path.dirname(__file__), "config.json")
    with open(filepath, "r") as f:
        config = json.load(f)
    logging.config.dictConfig(config)


setup_logger()


class LoggerRepo:

    def __init__(self, name: str) -> None:
        self.name = name
        self.logger: logging.Logger = logging.getLogger(self.name)

    def info(self, message: str, stacklevel: int = 1) -> None:
        self._log(logging.INFO, message, stacklevel=stacklevel)

    def error(self, message: str, stacklevel: int = 1) -> None:
        self._log(logging.ERROR, message, stacklevel=stacklevel, exc_info=True)

    def debug(self, message: str, stacklevel: int = 1):
        self._log(logging.DEBUG, message, stacklevel=stacklevel + 1)

    def _log(self, level: int, message: str, stacklevel: str = 1, exc_info: bool = False):
        self.logger.log(level=level, msg=message, stacklevel=stacklevel + 1, exc_info=exc_info)


__all__ = ["LoggerRepo"]
