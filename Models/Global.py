from enum import Enum


class FileFormat(Enum):
    XLSX = 0
    CSV = 1
    NONE = 2


class ErrorHandler(Enum):
    OK = 0
    NOT_OK = 1


class ExportFormat(Enum):
    DOCX = 0
    PDF = 1


MY_EXPORT_FORMAT = ExportFormat.DOCX
# MY_EXPORT_FORMAT = ExportFormat.PDF
