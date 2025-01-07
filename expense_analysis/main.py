import os
from workbook_builder import WorkbookBuilder
from etl import Transaction_Etl, get_user_home
from trans_db_api import TransactionDatabase

def refresh_project_data():
    for file in ['data.db','bk_download.xlsx']:
        project_path = os.path.join(os.getcwd(),file)
        expense_analysis_path = os.path.join(os.getcwd(), 'expense_analysis',file)

        if os.path.exists(project_path):
            os.remove(project_path)
        if os.path.exists(expense_analysis_path):
            os.remove(expense_analysis_path)

def main():
    refresh_project_data()

    etl = Transaction_Etl()
    etl.ingest('bk_download','csv')
    etl.transform()
    etl.load('data')

    db_path = os.path.join(os.getcwd(),"data.db")
    workbook_builder = WorkbookBuilder(TransactionDatabase(db_path))
    workbook_builder.build_workbook()

if __name__ == '__main__':
    main()