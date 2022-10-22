import os
from os import DirEntry
from typing import List

def get_bank_data_files() -> List[str]:
    bank_data_files = []

    if(user_home := os.environ.get('USERPROFILE')):

        print("User home: " + user_home)
        downloads_path = user_home + '\\Downloads'

        with os.scandir(downloads_path) as directory:

                csv_s = filter(is_csv,directory)
                csv_lines = set()

                for csv in csv_s:
                    with open(csv) as csv_handle:
                        for line in csv_handle:
                            csv_lines.add(line)

                csv_lines = list(csv_lines)
                csv_lines.sort(reverse=True)

                with open(user_home + '\\Repos\\automate-the-boring-stuff\\excel\\bk_download.csv','w') as master_csv:
                    for line in csv_lines:
                        master_csv.write(line)
                        

        

    else:
        print("Couldn't find user home.")

    return bank_data_files

def is_csv(file : DirEntry):
    return file.is_file() and file.name.endswith('.csv')


if __name__ == '__main__':
    get_bank_data_files()