from datetime import date
from hmac import trans_5C

class Transaction:

    def __init__(self):
        self._t_date = None
        self.d1 = None
        self.d2 = None
        self.category = None
        self.amount = None
        self.status = None

    @property
    def t_date(self):
        return self._t_date

    @t_date.setter
    def t_date(self, date_str : str):
        year, month, day = date_str.split('-')
        self._t_date = date(int(year),int(month),int(day))
