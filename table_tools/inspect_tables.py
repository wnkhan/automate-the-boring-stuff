import os
import pandas as pd

project_root = os.getcwd()
table_inspect_path = os.path.join(project_root,'data_ingestion','ingested')

def main():
    registered_actions = {'get_cols': get_columns,
                          'get_col': get_col,
                          'head': get_head}

    table_name = input("which table: ")
    action = input(f"which action {registered_actions.keys()}:")

    table = table_loader(table_name)

    registered_actions[action](table_name, table) 

def table_loader(table_name, path = None):
    if not path:
        path = os.path.join(table_inspect_path, table_name+'.csv')

    print(path)
    return pd.read_csv(path)

def get_columns(table_name, table: pd.DataFrame):
    print('table_name: ' + table_name)
    for col in table.columns:
        print(col)

def get_col(table_name, table: pd.DataFrame):
    print('table_name: ' + table_name)
    col_list_str =', '.join(table.columns.to_list())
    col_name = input('what column:\n' + col_list_str + '\n')
    limit = int(input('what limit: '))

    if limit:
        table = table.head(limit)

    for row in table[col_name]:
        print(row)

def get_head(table_name, table: pd.DataFrame):
    print('table_name: ' + table_name)
    print(table.head())

if __name__ == "__main__":
    main()