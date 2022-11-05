import pandas as pd
from trans_db_api import TransactionDatabase
from transaction import Transaction
from typing import List
import os

project_directory = os.environ.get('USERPROFILE') + '/Repos/automate-the-boring-stuff/' 

class TransactionExtractor:
    eating_out_categories = ["Coffee Shops","Restaurants", "Food & Dining", "Fast Food","Alcohol & Bars"]
    bill_and_utility_categories = ["car","Mobile Phone", "Rent", "Storage","Utilities"]
    subscriptions = ["Apple","Netflix","Spotify","ExpressVPN","Youtube","Medium",
                    "LinkedIn","Pluralsight","Game Pass","Prime"]

    def __init__(self):
        self.transactions = pd.read_csv(project_directory + 'excel/bk_download.csv')
        self.consolidate_eating_out()
        self.consolidate_bills_and_utilities()
        self.consolidate_subscriptions()

    def consolidate_eating_out(self) -> None:
        for eating_cat in TransactionExtractor.eating_out_categories:
            self.transactions['Category'].mask(self.transactions['Category'] == eating_cat, 'Eating Out',inplace=True)

    def consolidate_bills_and_utilities(self) -> None:
        for bill_cat in TransactionExtractor.bill_and_utility_categories: 
            self.transactions['Category'].mask(self.transactions['Category'] == bill_cat, 'Bills & Utilities',inplace=True)
        
    def consolidate_subscriptions(self) -> None:
        for sub_cat in TransactionExtractor.subscriptions:
            self.transactions.loc[self.transactions['Description']==sub_cat,'Category'] = 'Subscription'

    def get_transactions(self) -> List[Transaction]:
        return [Transaction(list(row[1:])) for row in self.transactions.itertuples()]



if __name__ == "__main__":
    extractor = TransactionExtractor()
    for trans in extractor.get_transactions():
        print(trans)