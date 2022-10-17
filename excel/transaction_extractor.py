from transaction import Transaction
import os

def get_transaction_data():
    transaction_list = []
    os.chdir('excel')

    with open('bk_download.csv','r') as download_handle:
        for idx, line in enumerate(download_handle):
            if idx != 0:
                line = purge_quoted_strings(line)
                line_items = line.strip().split(',')
                transaction_list.append(Transaction(line_items))

    return transaction_list

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
