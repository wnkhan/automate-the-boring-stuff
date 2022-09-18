import openpyxl as xl

def get_csv_file_data() -> None:
    wb = xl.Workbook()
    del wb['Sheet']
    wb.create_sheet('data')

    with open('bk_download.csv','r') as download_handle:
        for line in download_handle:
            purge_quoted_strings(line)
            line_items = line.strip().split()
            wb['data'].append(line_items)
    
    wb.save('bk_download.xlsx')

def purge_quoted_strings(line: str):
    start_pos = line.find('"')
    end_pos = line.find('"',start_pos + 1)
    first_quote = start_pos, end_pos

    start_pos = line.find('"',end_pos+1)
    end_pos = line.find('"',start_pos + 1)
    second_quote = start_pos, end_pos

    print('1: ' + line[first_quote[0]:first_quote[1]+1] + ' 2: ' + line[second_quote[0]:second_quote[1]+1])

def main():
    get_csv_file_data()


if __name__ == '__main__':
    main()