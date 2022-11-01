from trans_db_api import TransactionDatabase
from transaction_extractor import TransactionExtractor
from workbook_builder import WorkbookBuilder

def main():
    transaction_extractor = TransactionExtractor()
    transaction_db = TransactionDatabase('transaction.sqlite')

    for transaction in transaction_extractor.transaction_list:
        transaction_db.insert_transaction(transaction)
    

    workbook_builder = WorkbookBuilder(transaction_db)
    workbook_builder.build_workbook()

if __name__ == '__main__':
    main()