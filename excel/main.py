import openpyxl as xl
from transaction_extractor import TransactionExtractor
from workbook_builder import WorkbookBuilder

def main():
    transaction_extractor = TransactionExtractor()
    workbook_builder = WorkbookBuilder(transaction_extractor.transaction_list)
    workbook_builder.build_workbook()

if __name__ == '__main__':
    main()