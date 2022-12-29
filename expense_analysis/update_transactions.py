import os
import pandas as pd
from os import DirEntry
from trans_db_api import TransactionDatabase
from transaction import Transaction
from extractor import TransactionExtractor

def update_transaction_db_from_downloads() -> None: 
    bank_data_files = []

    if(user_home := os.environ.get('USERPROFILE')):
        with os.scandir(user_home +'\Downloads') as directory:
            csv_s = filter(is_csv,directory)

            bank_data_df_s = []
            for csv in csv_s:
                extractor = TransactionExtractor(csv_name = csv.path)
                bank_data_df_s.append(extractor.transactions)
            master_df = pd.concat(bank_data_df_s, ignore_index=True)

            category_pending_df = master_df.loc[master_df['Category'] == 'Category Pending']

            update_dict = {}
            for row in category_pending_df.itertuples():
                search_df = master_df.loc[(master_df['Amount'] == row[5])]
                if not search_df.empty:
                    update_dict.setdefault(row[0],search_df.iloc[0]['Category'])

            for key, value in update_dict.items():
                master_df.at[key,'Category'] = value

            master_df.drop_duplicates()

            all_transactions =  [Transaction(list(row[1:])) for row in master_df.itertuples()]

            trans_db = TransactionDatabase('transaction.sqlite')

            for trans in all_transactions:
                trans_db.insert_transaction(trans)

            
    else:
        print("Couldn't find user home.")

    return bank_data_files

def is_csv(file : DirEntry):
    return file.is_file() and file.name.endswith('.csv')


if __name__ == '__main__':
    update_transaction_db_from_downloads()