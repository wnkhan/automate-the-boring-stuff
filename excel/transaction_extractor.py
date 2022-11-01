from typing import List
from transaction import Transaction
import re
import os

class TransactionExtractor:
    eating_out_categories = ["Coffee Shops","Restaurants", "Food & Dining", "Fast Food","Alcohol & Bars"]
    bill_and_utility_categories = ["car","Mobile Phone", "Rent", "Storage","Utilities"]
    subscriptions = ["Apple","Netflix","Spotify","ExpressVPN","Youtube","Medium",
                    "LinkedIn","Pluralsight","Game Pass","Prime"]

    def __init__(self):
        self.transaction_list = []
        self.build_transaction_data_from_csv()
        self.consolidate_eating_out()
        self.consolidate_bills_and_utilities()
        self.consolidate_subscriptions()


    def build_transaction_data_from_csv(self):
        print('current working directory: ' + os.getcwd())
        project_dir = os.environ.get('USERPROFILE') + '\\Repos\\automate-the-boring-stuff\\'
        os.chdir(project_dir + 'excel')

        with open('bk_download.csv','r') as download_handle:
            for idx, line in enumerate(download_handle):
                if idx != 0:
                    line = purge_quoted_strings(line)
                    line_items = line.strip().split(',')
                    self.transaction_list.append(Transaction(line_items))


    def consolidate_eating_out(self):
        for trans in self.transaction_list:
            if re.search(self.build_regex(TransactionExtractor.eating_out_categories),trans.category,re.IGNORECASE):
                trans.category = "Eating Out"

    def consolidate_bills_and_utilities(self):
        for trans in self.transaction_list:
            if re.search(self.build_regex(TransactionExtractor.bill_and_utility_categories),trans.category,re.IGNORECASE):
                trans.category = "Bills & Utilities"

    def consolidate_subscriptions(self):
        for trans in self.transaction_list:
            if re.search(self.build_regex(TransactionExtractor.subscriptions),trans.d1,re.IGNORECASE):
                trans.category = "Subscriptions"

    @staticmethod
    def build_regex(target_strs : List[str]):
        result = ""
        for index, sub in enumerate(target_strs):
            if index < len(target_strs) - 1:
                result += sub + "|"
            else:
                result += sub
        return result



def purge_quoted_strings(line: str):
    start_pos = line.find('"')
    end_pos = line.find('"',start_pos + 1)
    first_quote = start_pos, end_pos
    modified_quote1 = line[first_quote[0]:first_quote[1]].replace(',',';')

    start_pos = line.find('"',end_pos+1)
    end_pos = line.find('"',start_pos + 1)
    second_quote = start_pos, end_pos
    modified_quote2 = line[second_quote[0]:second_quote[1]].replace(',',';')

    return line[:first_quote[0]] + modified_quote1 + line[first_quote[1]:second_quote[0]] + modified_quote2 + line[second_quote[1]:]
