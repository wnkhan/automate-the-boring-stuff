import os
import pandas as pd
from os import DirEntry
from typing import List

def get_bank_data_files() -> List[str]:
    bank_data_files = []

    if(user_home := os.environ.get('USERPROFILE')):
        with os.scandir(user_home +'\Downloads') as directory:
            csv_s = filter(is_csv,directory)

            bank_data_df_s = []
            for csv in csv_s:
                df = pd.read_csv(csv)
                bank_data_df_s.append(df)
            master_df = pd.concat(bank_data_df_s, ignore_index=True)

            category_pending_df = master_df.loc[master_df['Category'] == 'Category Pending']

            update_dict = {}
            for row in category_pending_df.itertuples():
                search_df = master_df.loc[(master_df['Date'] == row[1]) & (master_df['Description'] == row[2])]
                update_dict.setdefault(row[0],search_df.iloc[0]['Category'])

            for key, value in update_dict.items():
                master_df.at[key,'Category'] = value

            master_df.drop_duplicates()
            master_df.to_csv(os.path.join(user_home,'Repos','automate-the-boring-stuff','excel','bk_download.csv'), index=False)
    else:
        print("Couldn't find user home.")

    return bank_data_files

def is_csv(file : DirEntry):
    return file.is_file() and file.name.endswith('.csv')


if __name__ == '__main__':
    get_bank_data_files()