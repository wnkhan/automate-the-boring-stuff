import pandas as pd
from trans_db_api import TransactionDatabase
from transaction import Transaction
from typing import List


class TransactionExtractor:
    eating_out_categories = ["Coffee Shops","Restaurants", 
                             "Food & Dining", "Fast Food",
                             "Food Dining","Alcohol & Bars"]


    public_trans_descriptions = ["Indego"]


    bill_and_utility_categories = ["Car","Mobile Phone", 
                                   "Rent", "Storage",
                                   "Utilities","Internet"]

    bill_and_utility_descriptions = ["Fi"]

    subscriptions = ["Apple","Netflix",
                     "Spotify","ExpressVPN",
                     "Youtube","Medium",
                    "LinkedIn","Pluralsight",
                    "Game Pass","Prime","Amznfreetime"]

    shopping = ['Electronics & Software','Pet Food & Supplies','Clothing']

    def __init__(self, csv_name: str):
        self.transactions = pd.read_csv(csv_name)
        self.consolidate_eating_out()
        self.consolidate_bills_and_utilities()
        self.consolidate_subscriptions()
        self.consolidate_public_trans()
        self.consolidate_shopping()
        self.remove_usaa_transfers()

    def consolidate_eating_out(self) -> None:
        for eating_cat in TransactionExtractor.eating_out_categories:
            self.transactions['Category'].mask(self.transactions['Category'] == eating_cat, 'Eating Out',inplace=True)

    def consolidate_public_trans(self) -> None:
        for trans_descr in TransactionExtractor.public_trans_descriptions:
            self.transactions.loc[self.transactions['Description'].str.contains(trans_descr),'Category'] = 'Public Transportation'

    def consolidate_bills_and_utilities(self) -> None:
        for bill_cat in TransactionExtractor.bill_and_utility_categories: 
            self.transactions['Category'].mask(self.transactions['Category'] == bill_cat, 'Bills & Utilities',inplace=True)
        for bill_descr in TransactionExtractor.bill_and_utility_descriptions:
            self.transactions.loc[self.transactions['Description'].str.contains(bill_descr),'Category'] = 'Bills & Utilities'

    def consolidate_subscriptions(self) -> None:
        for sub_cat in TransactionExtractor.subscriptions:
            self.transactions.loc[self.transactions['Description'].str.contains(sub_cat),'Category'] = 'Subscription'

    def consolidate_shopping(self) -> None:
        for shopping_cat in TransactionExtractor.shopping:
            self.transactions['Category'].mask(self.transactions['Category'] == shopping_cat, 'Shopping',inplace=True)

    def remove_usaa_transfers(self) -> None:
        selected = self.transactions.query('"USAA Transfer" in Description and Amount < 0')
        print('Removed:')
        print(selected.head())
        self.transactions.drop(selected.index,inplace=True)

    def get_transactions(self) -> List[Transaction]:
        return [Transaction(list(row[1:])) for row in self.transactions.itertuples()]
