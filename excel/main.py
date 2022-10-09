import openpyxl as xl
from data_converter import get_transaction_data
from workbook_builder import WorkbookBuilder

def main():
    workbook_builder = WorkbookBuilder(get_transaction_data())
    workbook_builder.build_workbook()

if __name__ == '__main__':
    main()