import sqlite3
from typing import List
from transaction import Transaction
import os

project_directory = os.getcwd()

class TransactionDatabase:
    
    def __init__(self,database_name : str):
        self.insertion_count = 1
        self.connection = sqlite3.connect(os.path.join(project_directory,database_name))
        self.cursor = self.connection.cursor()
        try:
            table = """ CREATE TABLE transactions(
                        id INTEGER,
                        day INTEGER,
                        month INTEGER,
                        year INTEGER,
                        d1 TEXT,
                        d2 TEXT,
                        category TEXT,
                        amount REAL,
                        status TEXT
                    );"""
            self.cursor.execute(table)
        except sqlite3.OperationalError:
            print("transaction table already created.")

    def insert_transaction(self, transaction : Transaction):
        try:
            if(not (in_table := self.is_transaction_in_table(transaction))):
                sql_query = f"""
                        INSERT INTO transactions
                        VALUES ({self.insertion_count},{transaction.t_date.day},{transaction.t_date.month},{transaction.t_date.year},"{transaction.d1}","{transaction.d2}",
                        "{transaction.category}",{transaction.amount},"{transaction.status}")
                        """
                self.cursor.execute(sql_query)
                self.connection.commit()
                self.insertion_count+=1
        except:
            print("Insertion failed.")
            print(sql_query)

    def is_transaction_in_table(self, transaction : Transaction) -> bool:
        try:
            sql_query = f"""
                        SELECT *
                        FROM transactions
                        WHERE year = {transaction.t_date.year} AND month = {transaction.t_date.month} AND day = {transaction.t_date.day}
                        AND d1 = "{transaction.d1}" AND d2 = "{transaction.d2}" AND amount = {transaction.amount}
                        """
            self.cursor.execute(sql_query) 
            return len(self.cursor.fetchall()) != 0
        except sqlite3.OperationalError:
            print("Skipping insertion of the following transaction: " + str(transaction))
            return True

    def get_all_transactions(self) -> List[Transaction]:
        self.cursor.execute("""
        SELECT *
        FROM transactions
        """)
        fetched = self.cursor.fetchall()
        return [self.tuple_to_transaction(row) for row in fetched]

    def get_transaction_by_category(self,category):
        self.cursor.execute(f"""
        SELECT *
        FROM transactions
        WHERE category = "{category}"
        """)
        return self.cursor.fetchall()

    def get_transactions_by_month(self,month,year):
        self.cursor.execute(f"""
        SELECT *
        FROM transactions
        WHERE month = {month} AND year = {year}
        """)
        fetched = self.cursor.fetchall()
        return [self.tuple_to_transaction(row) for row in fetched]

    def get_categories_by_month(self,month,year):
        query = f"""
        SELECT DISTINCT category
        FROM transactions
        WHERE month = {month} AND year = {year}
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_monthly_category_total(self,month_year,category):
        month, year = month_year.split('-')
        cat = str(category)
        query = f"""
        SELECT SUM(amount)
        FROM transactions
        WHERE month = {month} AND year = {year} AND category = '{category}'
        """
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def get_unique_month_and_years(self):
        query = """
        SELECT DISTINCT month, year 
        FROM transactions
        """
        self.cursor.execute(query)
        
        month_and_years = []
        for month, year in self.cursor.fetchall():
            month_and_years.append(f'{month}-{year}')
        
        return month_and_years


    def delete_transaction_by_name(self,name):
        self.cursor.execute(f"""
        DELETE FROM transaction
        WHERE name = "{name}"
        """)
        self.connection.commit()

    def tuple_to_transaction(self,tran_tuple):
        trans_data = [str(tran_tuple[3])+"-"+str(tran_tuple[2])+"-"+str(tran_tuple[1]),tran_tuple[4],tran_tuple[5],tran_tuple[6],tran_tuple[7],tran_tuple[8]]
        return Transaction(transaction_data=trans_data)

    def __del__(self):
        self.connection.close()