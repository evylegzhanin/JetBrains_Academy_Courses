import re
import argparse
import os

check_funcs = ['length_check(line, index, path)',
               'indentation_check(line, index, path)',
               'semicolon_check(line, index, path)',
               'two_spaces_before_inline_comment_check(line, index, path)',
               'todo_check(line, index, path)',
               'two_blank_lines_before_line_check(line, index, lines, path)',
               'spaces_after_construction_name_check(line, index, path)',
               'camel_case_in_class_name_check(line, index, path)',
               'snake_case_in_function_name_check(line, index, path)']

issues_dict = {'S001': 'Too long',
               'S002': 'Indentation is not a multiple of four',
               'S003': 'Unnecessary semicolon',
               'S004': 'At least two spaces required before inline comments',
               'S005': 'TODO found',
               'S006': 'More than two blank lines used before this line',
               'S007': "Too many spaces after '$construction'",
               'S008': "'Class name '$name' should be written in CamelCase'",
               'S009': "Function name '$name' should be written in snake_case"}


def length_check(line, index, path):
    if len(line) > 79:
        return f'{path}: Line {index}: S001 {issues_dict["S001"]}'


def indentation_check(line, index, path):
    if line.strip() != '':
        spaces = re.search(r'^\s+', line)
        if spaces is not None and len(spaces[0]) % 4 != 0:
            return f'{path}: Line {index}: S002 {issues_dict["S002"]}'


def semicolon_check(line, index, path):
    if (';' in line) and (re.search(r'#.*;|[\'\"].*;.*[\'\"]', line) is None):
        return f'{path}: Line {index}: S003 {issues_dict["S003"]}'


def two_spaces_before_inline_comment_check(line, index, path):
    if ('#' in line) and (re.search(r'\s{2,}#\s|^\s*#', line) is None):
        return f'{path}: Line {index}: S004 {issues_dict["S004"]}'


def todo_check(line, index, path):
    if re.search(r'#\s[tT][oO][dD][oO]', line) is not None:
        return f'{path}: Line {index}: S005 {issues_dict["S005"]}'


def two_blank_lines_before_line_check(line, index, lines, path):
    index_ = index - 1
    if index_ >= 3 and line.strip() != '':
        if ''.join(lines[index_ - 3:index_]).strip() == '':
            return f'{path}: Line {index}: S006 {issues_dict["S006"]}'


def spaces_after_construction_name_check(line, index, path):
    pattern = r'^\s*(def|class)\s{2,}([a-zA-Z0-9_-]+)'
    if re.search(pattern, line) is not None:
        construction = re.search(pattern, line).group(1)
        return f'{path}: Line {index}: S007 {issues_dict["S007"].replace("$construction", construction)}'


def camel_case_in_class_name_check(line, index, path):
    if line.startswith('class ') and (re.search(r'^\s*class\s+([A-Z][a-zA-Z0-9]*)', line) is None):
        name = re.search(r'^\s*class\s+([a-zA-Z0-9_-]*)', line).group(1)
        return f'{path}: Line {index}: S008 {issues_dict["S008"].replace("$name", name)}'


def snake_case_in_function_name_check(line, index, path):
    if line.startswith('def ') and (re.search(r'^\s*def\s+[a-z_][a-z0-9_]*', line) is None):
        name = re.search(r'^\s*def\s+([a-zA-Z0-9_-]+)', line).group(1)
        return f'{path}: Line {index}: S009 {issues_dict["S009"].replace("$name", name)}'


def print_issues_from_file(path):
    with open(path, 'r') as file:
        lines = file.readlines()
        for index, line in enumerate(lines, start=1):
            for func in check_funcs:
                issue = eval(func)
                if issue is not None:
                    print(issue)


def parse_dir(path):
    entries = sorted(os.listdir(path))
    paths = []
    for entry in entries:
        path_to_file = os.path.join(path, entry)
        if os.path.isdir(path_to_file):
            parse_dir(path_to_file)
        if os.path.isfile(path_to_file):
            paths.append(path_to_file)
    return paths


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('path')
    args = parser.parse_args()
    path = args.path

    if os.path.isfile(path):
        print_issues_from_file(path)
    elif os.path.isdir(path):
        paths = parse_dir(path)
        [print_issues_from_file(path) for path in paths]


if __name__ == '__main__':
    main()