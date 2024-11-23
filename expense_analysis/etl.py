import os
import platform
import pandas as pd
import sqlite3
from field_masks import category_mappings, description_mappings


def get_user_home():
    user_home = None

    if platform.system() in ['Darwin','Linux']:
        user_home = os.environ.get('HOME')
    elif platform.system() == "Windows":
        user_home = os.environ.get('USERPROFILE')

    return user_home

class Transaction_Etl:

    def __init__(self):
        self.df = None

    def ingest(self, table_name, extension, path=os.path.join(get_user_home(),"Downloads")):
        match extension:
            case "csv":
                self.df = pd.read_csv(os.path.join(path,".".join([table_name,extension])))
            case "tsv":
                self.df = pd.read_table(os.path.join(path,".".join(table_name,extension)))


    def transform(self):
        for category, mapping_list in category_mappings.items():
            self.df.loc[self.df['Category'].isin(mapping_list),'Category'] = category

        for category, mapping_list in description_mappings.items():
            self.df.loc[self.df['Description'].isin(mapping_list), 'Category'] = category

        self.df['id'] = range(1, len(self.df) + 1)
        self.df['month'] = self.df['Date'].apply(lambda date_str: date_str.split('-')[1])
        self.df['year'] = self.df['Date'].apply(lambda date_str: date_str.split('-')[0])
        self.df['day'] = self.df['Date'].apply(lambda date_str: date_str.split('-')[2])
        self.df.rename(columns={'Description':'d1', 
                                'Original Description': 'd2', 
                                'Category': 'category',
                                'Amount':'amount',
                                'Status':'status'},
                        inplace=True)

        column_ordering = ['id','day','month','year','d1','d2','category','amount','status']
        self.df = self.df[column_ordering]

    def load(self, db_name):
        with sqlite3.connect(".".join([db_name,"db"])) as conn:
            self.df.to_sql('transactions',conn,if_exists='replace',index=False)
        