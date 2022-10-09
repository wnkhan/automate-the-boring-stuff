from datetime import date

class Transaction:

    def __init__(self):
        self._t_date = None
        self.d1 = None
        self.d2 = None
        self.category = None
        self.amount = None
        self.status = None

    def __init__(self, transaction_data : list):
        self.t_date = transaction_data[0]
        self.d1 = transaction_data[1]
        self.d2 = transaction_data[2]
        self.category = transaction_data[3]
        self.amount = transaction_data[4]
        self.status = transaction_data[5]

    def __str__(self) -> str:
        return str(self.t_date) + ',' + self.d1 + ',' + self.category + ',' + self.amount + ',' + self.status 

    @property
    def t_date(self):
        return self._t_date

    @t_date.setter
    def t_date(self, date_str : str):
        year, month, day = date_str.split('-')
        self._t_date = date(int(year),int(month),int(day))
