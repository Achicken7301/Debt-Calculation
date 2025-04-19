from enum import Enum, auto



class FileFormat(Enum):
    XLSX = auto()
    CSV = auto()
    NONE = auto()


class ErrorHandler(Enum):
    OK = 0
    NOT_OK = 1


class ExportFormat(Enum):
    DOCX = "DOCX"
    PDF = "PDF"
    EXCEL = "EXCEL"


class Section(Enum):
    GENERAL = "GENERAL"
    STORE = "STORE"


class Option(Enum):
    language = "language"
    export_format = "export_format"
    name = "name"
    addr = "addr"
    street = "street"
    district = "district"
    province = "province"
    city = "city"
    phone = "phone"
    director = "director"
    co_founder = "co_founder"

# conf = ProgramConfig()
# # I dont know how to not hard code here
# if (
#     conf.read(Section.GENERAL.value, Option.export_format.value)
#     == ExportFormat.DOCX.value
# ):
#     conf.set_export_format(ExportFormat.DOCX)
# else:
#     conf.set_export_format(ExportFormat.PDF)
