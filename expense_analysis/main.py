import os
from workbook_builder import WorkbookBuilder
from etl import Transaction_Etl
from trans_db_api import TransactionDatabase

def main():
    etl = Transaction_Etl()
    etl.ingest('bk_download','csv')
    etl.transform()
    etl.load('data')

    db_path = os.path.join(os.getcwd(),"data.db")
    workbook_builder = WorkbookBuilder(TransactionDatabase(db_path))
    workbook_builder.build_workbook()

if __name__ == '__main__':
    main()