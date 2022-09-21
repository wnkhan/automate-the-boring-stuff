import openpyxl as xl
import os

def get_csv_file_data() -> None:
    os.chdir('excel')
    wb = xl.Workbook()
    del wb['Sheet']
    wb.create_sheet('data')

    with open('bk_download.csv','r') as download_handle:
        for line in download_handle:
            line = purge_quoted_strings(line)
            line_items = line.strip().split(',')
            print(line_items)
            wb['data'].append(line_items)
    
    wb.save('bk_download.xlsx')

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

def main():
    get_csv_file_data()


if __name__ == '__main__':
    main()