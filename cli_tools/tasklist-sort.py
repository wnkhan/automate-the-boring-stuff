from string import whitespace
import subprocess 
import re
from argparse import ArgumentParser 
from sys import stdout

def main():
    script_args = get_args()

    tasklist_process = subprocess.Popen('tasklist',stdout=subprocess.PIPE)

    std_out, std_error = tasklist_process.communicate()

    all_lines = str(std_out,encoding='utf-8').strip().split('\n')

    header, header_separator, *lines  = all_lines

    task_list_strings = cleanse_thy_data(lines)

    if script_args.sort_type == 'name':
        task_list_strings.sort(key=lambda task_string : task_string[0].lower())
    elif script_args.sort_type == 'mem_usage':
        task_list_strings.sort(key=lambda task_string : convert_to_int(task_string[4]))

    for task_item in task_list_strings:
        print('{:<25} {:>9} {:>10} {:>4} {:>9} {}'.format(*task_item))


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

    return whitespace_purged_matches

def convert_to_int(value : str) -> int:
    stripped = value.strip().replace(',','')
    return int(stripped)


def get_args():
    parser = ArgumentParser(description="Module for providing task list sorting functionality")
    parser.add_argument("--sort",dest="sort_type",default="name",help="valid options: name, mem_usage")
    return parser.parse_args()

if __name__ == "__main__":
    main()