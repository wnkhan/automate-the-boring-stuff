from trans_db_api import TransactionDatabase
from workbook_builder import WorkbookBuilder

def main():
    transaction_db = TransactionDatabase('transaction.sqlite')
    workbook_builder = WorkbookBuilder(transaction_db)
    workbook_builder.build_workbook()

if __name__ == '__main__':
    main()