from unicodedata import category
import openpyxl as xl
from openpyxl.chart import (PieChart,Reference)
from typing import List
from datetime import date
from transaction import Transaction

class WorkbookBuilder:
    def __init__(self, transaction_list : List[Transaction]):
        self.transaction_list = transaction_list
        self.monthly_transactions = {}
        self.monthly_transactions_by_category = {}

    def get_sheetnames(self) -> List[str]:
        transaction_dates = [get_month_and_year(trans.t_date) for trans in self.transaction_list]
        date_set = set(transaction_dates)
        sheetnames = list(date_set)
        sheetnames.sort()

        return sheetnames

    def get_categories(self) -> List[str]:
        return set([trans.category for trans in self.transaction_list])

    def update_workbook_data(self) -> None:
        for sheet in self.get_sheetnames():
            if self.monthly_transactions.get(sheet) is None:
                self.monthly_transactions[sheet] = [] 
            if self.monthly_transactions_by_category.get(sheet) is None:
                self.monthly_transactions_by_category[sheet] = {}
                for category in self.get_categories():
                    self.monthly_transactions_by_category[sheet][category] = 0.0
        for trans in self.transaction_list:
            month_and_year = get_month_and_year(trans.t_date)
            if self.monthly_transactions.get(month_and_year) is not None:
                self.monthly_transactions[month_and_year].append(trans)
            self.monthly_transactions_by_category[month_and_year][trans.category] += float(trans.amount)

            

    def build_workbook(self) -> None:
        self.update_workbook_data()

        wb = xl.Workbook()
        del wb['Sheet']

        for sheet in self.get_sheetnames():
            wb.create_sheet(sheet)
            wb.create_sheet(sheet+"-categories")

            sorted_list = sorted(self.monthly_transactions[sheet], key = lambda trans : trans.category)
            for trans in sorted_list:
                trans_details = [trans.t_date,trans.d1,trans.category,float(trans.amount),trans.status]
                wb[sheet].append(trans_details)

            for category in self.get_categories():
                category_amount = self.monthly_transactions_by_category[sheet][category]
                category_row = [category,category_amount]
                if category_amount < 0:
                    wb[sheet+"-categories"].append(category_row)

            pie = PieChart()
            labels = Reference(wb[sheet+"-categories"],min_col=1,min_row=1,max_row=len(self.get_categories()))
            data = Reference(wb[sheet+"-categories"],min_col=2,min_row=1,max_row=len(self.get_categories()))
            pie.add_data(data,titles_from_data=False)
            pie.set_categories(labels)
            pie.title = "Spending by Category"
            wb[sheet+"-categories"].add_chart(pie,"G1")

        wb.save('bk_download.xlsx')

def get_month_and_year(transaction_date : date) -> str:
    return f'{transaction_date.month}-{transaction_date.year}'

