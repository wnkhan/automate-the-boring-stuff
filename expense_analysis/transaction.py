from datetime import date
import pandas as pd

def get_separator(input_str: str):
    date_separators = ['\\','-','/']
    for date_sep in date_separators:
        if date_sep in input_str:
            return date_sep
class Transaction:

    def __init__(self, transaction_data):
        if isinstance(transaction_data,pd.Series):
            self.t_date = transaction_data.Date
            self.d1 = transaction_data.Description
            self.d2 = transaction_data['Original Description']
            self.category = transaction_data.Category
            self.amount = transaction_data.Amount
            self.status = transaction_data.Status
        elif isinstance(transaction_data,list):
            self.t_date = transaction_data[0]
            self.d1 = transaction_data[1]
            self.d2 = transaction_data[2]
            self.category = transaction_data[3]
            self.amount = transaction_data[4]
            self.status = transaction_data[5]

    def __str__(self) -> str:
        return str(self.t_date) + ',' + self.d1 + ',' + self.category + ',' + str(self.amount) + ',' + self.status 

    @property
    def t_date(self):
        return self._t_date

    @t_date.setter
    def t_date(self, date_str : str):
        if sep := get_separator(date_str):
            if '-' in sep:
                year, month, day = date_str.split(sep)
                self._t_date = date(int(year),int(month),int(day))
            elif '\\' in sep or '/' in sep:
                month, day, year = date_str.split(sep)
                self._t_date = date(int(year),int(month),int(day))