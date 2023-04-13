# Expense Analysis Project
The expense_analysis directory contains a project that demonstrates how to ingest bank transaction data and generate an Excel workbook with monthly expense and income information.

# Dependencies
This project uses the pandas and openpyxl Python packages, which can be installed using pip:

```shell
pip install pandas openpyxl
```

# Usage
1. Updating Transactions
Before generating the Excel workbook, you will need to update the local database with your bank transactions. To do this, you can use the update_transactions.py script. This script assumes that your bank transaction data is in a CSV file with the following columns: Date, Description, and Amount.

To update the local database, navigate to the expense_analysis directory and run the following command:

```shell
python update_transactions.py --input_file <path_to_input_file>
```

This will insert the transactions from the specified CSV file into a SQLite database named transactions.db, which will be created in the same directory as the script.

2. Generating Excel Workbook
Once you have updated the local database with your transactions, you can generate an Excel workbook containing monthly expense and income information using the main.py script.

To generate the Excel workbook, navigate to the expense_analysis directory and run the following command:

```python
python main.py --output_file <path_to_output_file>
```

This will generate an Excel workbook containing monthly expense and income information, which will be saved to the specified output_file.

3. Shell Scripts
For convenience, there are two shell scripts provided: update_transactions.sh and generate_report.sh. These scripts can be used to run the update_transactions.py and main.py scripts, respectively.

# Running on Windows
On Windows, you can use the update_transactions.bat and generate_report.bat batch files instead.

To use the shell scripts, navigate to the expense_analysis directory and run the following command:

```bash
./<script_name.sh>
```

# Notes
This project is intended as a starting point for building your own expense analysis tool. You may need to modify the code to fit your specific use case.
The update_transactions.py script assumes that the transactions in the CSV file have not already been inserted into the database. If you need to update transactions that have already been inserted, you will need to modify the script to handle duplicates.
The output_file argument for main.py should have a .xlsx extension, as the generated workbook will be in Excel format.
The database schema and queries used in this project are intended as examples and may need to be modified to fit your specific use case.


