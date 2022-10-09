from unicodedata import category
import openpyxl as xl
from typing import List
from datetime import date
from transaction import Transaction

class WorkbookBuilder:
    def __init__(self, transaction_list : List[Transaction]):
        self.transaction_list = transaction_list
        self.monthly_transactions = {}

    def get_sheetnames(self) -> List[str]:
        transaction_dates = [get_month_and_year(trans.t_date) for trans in self.transaction_list]
        date_set = set(transaction_dates)
        sheetnames = list(date_set)
        sheetnames.sort()

        return sheetnames

    def update_workbook_data(self) -> None:
        for sheet in self.get_sheetnames():
            if self.monthly_transactions.get(sheet) is None:
                self.monthly_transactions[sheet] = [] 
        for trans in self.transaction_list:
            month_and_year = get_month_and_year(trans.t_date)
            if self.monthly_transactions.get(month_and_year) is not None:
                self.monthly_transactions[month_and_year].append(trans)

    def build_workbook(self) -> None:
        self.update_workbook_data()

        wb = xl.Workbook()
        del wb['Sheet']

        for sheet in self.get_sheetnames():
            wb.create_sheet(sheet)
            sorted_list = sorted(self.monthly_transactions[sheet], key = lambda trans : trans.category)
            for trans in sorted_list:
                trans_details = [trans.t_date,trans.d1,trans.category,float(trans.amount),trans.status]
                wb[sheet].append(trans_details)

        wb.save('bk_download.xlsx')

def get_month_and_year(transaction_date : date) -> str:
    return f'{transaction_date.month}-{transaction_date.year}'

