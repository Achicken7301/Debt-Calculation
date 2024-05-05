from enum import Enum


class FileFormat(Enum):
    XLSX = 0
    CSV = 1
    NONE = 2


class ErrorHandler(Enum):
    OK = 0
    NOT_OK = 1
