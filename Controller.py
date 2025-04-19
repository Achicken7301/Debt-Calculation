
from Models.ExcelModel import ExcelModel


class Controller:
    def __init__(self):
        self.e_m = ExcelModel()

    def generate_xlsx_format(self, raw_data, closing_date, i:float):
        """This will execute the ExcelModel and return the final something, i dont know yet!!!
        """ 
        self.e_m.export(raw_data, closing_date, i)