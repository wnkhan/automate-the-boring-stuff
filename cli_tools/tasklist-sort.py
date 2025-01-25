import subprocess 
import re
from argparse import ArgumentParser 
import pandas as pd

def main():
    script_args = get_args()

    header, *lines  = get_cmd_output('tasklist')

    task_list_strings = cleanse_thy_data(lines)

    task_list_df = create_task_list_dataframe(parse_header(header),task_list_strings)

    col_mapping = {'name':'Image Name','mem_usage':'Mem Usage','pid':'PID','sesh_name':'Session Name'}

    sort_cols = [col_mapping[col] for col in script_args.sort_type]

    task_list_df.sort_values(by=sort_cols,inplace=True)    

    print(task_list_df.to_string(index=False))


def create_task_list_dataframe(header, task_list_strings: list) -> list:
    task_list_df = pd.DataFrame(task_list_strings,columns=header)
    return task_list_df

def parse_header(header: str) -> list:
    column_labels = re.split(r'\s{2,}+',header.strip())
    column_labels.insert(2, ' '.join(column_labels[1].split()[1:]))
    column_labels[1] = column_labels[1].split()[0]
    return column_labels

def display_data(header: str, header_sep: str, task_rows: list):
    print(header)
    print(header_sep)
    for task_item in task_rows:
        print('{:<25} {:>8} {:>16} {:>10} {:>10} {}'.format(*task_item))

def get_cmd_output(command: str) -> list:
    tasklist_process = subprocess.Popen(command,stdout=subprocess.PIPE)

    std_out, std_error = tasklist_process.communicate()

    return str(std_out,encoding='utf-8').strip().split('\n')
    
def cleanse_thy_data(data : list) -> list:
    tasklist_regex = "([a-zA-Z. ]+[^\s$])(\s+)([0-9]+)(\s)([a-zA-Z]+)(\s+)([0-9]+)(\s+)([0-9,]+)(\s+)([kK])"
    matches = [match for line in data if (match := re.match(tasklist_regex,line))]

    whitespace_purged_matches = []

    for match in matches:
        purged_match = []
        for group in match.groups():
            if not group.isspace():
                purged_match.append(group) 
        if purged_match:
            whitespace_purged_matches.append(purged_match)

    whitespace_purged_matches = [item[0:4] + [' '.join(item[4:])] for item in whitespace_purged_matches]
    return whitespace_purged_matches

def convert_to_int(value : str) -> int:
    stripped = value.strip().replace(',','')
    return int(stripped)


def get_args():
    parser = ArgumentParser(description="Module for providing task list sorting functionality")
    parser.add_argument("--sort", dest="sort_type", nargs='+', default=["name"], help="valid options: name, mem_usage, pid")
    return parser.parse_args()

if __name__ == "__main__":
    main()