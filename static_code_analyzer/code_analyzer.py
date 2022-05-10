import re
import sys
import os
import ast
from collections import defaultdict


class CodeAnalyser:

    errors = {
        'S001': 'Too long',
        'S002': 'Indentation is not a multiple of four',
        'S003': 'Unnecessary semicolon after a statement',
        'S004': 'Less than two spaces before inline comments',
        'S005': 'TODO found',
        'S006': 'More than two blank lines preceding a code line',
        'S007': 'Too many spaces after construction_name',
        'S008': 'Class name class_name should be written in CamelCase',
        'S009': 'Function name function_name should be written in snake_case',
        'S010': 'Argument name arg_name should be written in snake_case',
        'S011': 'Variable var_name should be written in snake_case',
        'S012': 'The default argument value is mutable'
    }

    def check_code(self, path_to_file):
        self.path_to_file = path_to_file
        self.desc_line_type = []
        self.n_blank_line = 0
        self.report = defaultdict(list)

        CodeAnalyser.new_check_code(self, self.path_to_file)

        with open(self.path_to_file, 'r') as f:
            for n_line, line in enumerate(f.readlines(), start=1):
                line_type = CodeAnalyser.get_type_of_line(self, line)
                self.desc_line_type.append(line_type)
                CodeAnalyser.check_len_line(self, n_line, line, 'S001')
                CodeAnalyser.check_indent(self, n_line, line, 'S002')
                CodeAnalyser.check_semi_colon(self, n_line, line, 'S003')
                if line_type == 'inline_comment':
                    CodeAnalyser.check_space_before_inline_comment(self, n_line, line, 'S004')
                CodeAnalyser.check_todo(self, n_line, line, 'S005')
                CodeAnalyser.check_blanks_lines(self, n_line, line, 'S006')
                CodeAnalyser.check_blanks_after_func_class(self, n_line, line, 'S007')
                CodeAnalyser.check_camel_case(self, n_line, line, 'S008')
                CodeAnalyser.check_snake_case(self, n_line, line, 'S009')

        CodeAnalyser.print_report(self)

    def new_check_code(self, path_to_file):
        with open(path_to_file, 'r') as f:
            script = f.read()
        tree = ast.parse(script)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for arg in node.args.args:
                    CodeAnalyser.new_check_snake_case(self, arg.arg, "S010", node.lineno)
                for arg in node.args.defaults:
                    if isinstance(arg, ast.List):
                        CodeAnalyser.set_report(self, node.lineno, "S012")
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                CodeAnalyser.new_check_snake_case(self, node.id, "S011", node.lineno)

    def new_check_snake_case(self, name, error_code, n_line):
        if re.search(r'^[a-z_]{1,2}[a-z0-9_]*[_]{0,2}$', name) is None:
            CodeAnalyser.set_report(self, n_line, error_code)

    def get_type_of_line(self, line):
        if re.match(r'^$', line):
            self.n_blank_line += 1
            return 'blank_line'

        if re.match(r'^ *#', line):
            return 'comment'

        if re.match(r'.*#.*', line):
            return 'inline_comment'

        return 'code'

    def check_indent(self, n_line, line, error_code):
        if len(re.search(r'^ *', line).group(0)) % 4 != 0:
            CodeAnalyser.set_report(self, n_line, error_code)

    def check_len_line(self, n_line, line, error_code):
        if len(line) > 79:
            CodeAnalyser.set_report(self, n_line, error_code)

    def check_semi_colon(self, n_line, line, error_code):
        if self.desc_line_type[n_line - 1] == 'code':
            if re.search(r';$', line):
                CodeAnalyser.set_report(self, n_line, error_code)
        if self.desc_line_type[n_line - 1] == 'inline_comment':
            if re.search(r'.*;.*#', line):
                CodeAnalyser.set_report(self, n_line, error_code)

    def check_space_before_inline_comment(self, n_line, line, error_code):
        if self.desc_line_type[n_line - 1] == 'inline_comment':
            if re.search(r' {2}#', line) is None:
                CodeAnalyser.set_report(self, n_line, error_code)

    def check_todo(self, n_line, line, error_code):
        if re.search(r'#.*todo', line, re.IGNORECASE):
            CodeAnalyser.set_report(self, n_line, error_code)

    def check_blanks_lines(self, n_line, line, error_code):
        if self.desc_line_type[n_line - 1] != 'blank_line':
            if self.n_blank_line > 2:
                CodeAnalyser.set_report(self, n_line, error_code)
            self.n_blank_line = 0

    def check_blanks_after_func_class(self, n_line, line, error_code):
        result = re.search(r'^ *(?P<constructor>def|class)(?P<space> *)', line)
        if result is not None and len(result.group('space')) > 1:
            CodeAnalyser.set_report(self, n_line, error_code)

    def check_camel_case(self, n_line, line, error_code):
        if re.search(r'^class *', line):
            if re.search(r'(?P<constructor>class) *[A-Z]([a-zA-Z0-9])*', line) is None:
                CodeAnalyser.set_report(self, n_line, error_code)

    def check_snake_case(self, n_line, line, error_code):
        if re.search(r'(^| *)def *', line):
            if re.search(r'def *[a-z_]{1,2}([a-z0-9_]*[_]{0,2})', line) is None:
                CodeAnalyser.set_report(self, n_line, error_code)

    def set_report(self, n_line, error_code):
        self.report[n_line].append(error_code)
       
    def print_report(self):
        for k, v in self.report.items():
            for elt in v:
                print(f'{self.path_to_file}: Line {k}: {elt} {CodeAnalyser.errors[elt]}')

path_to_file = sys.argv[1]
analyzer = CodeAnalyser()
list_files = []
if os.path.isfile(path_to_file):
    analyzer.check_code(path_to_file)
else:
    for dirpath, dirnames, files in os.walk(path_to_file, topdown=True):
        for file in files:
            list_files.append(os.path.join(dirpath, file))

    for file in sorted(list_files):
        analyzer.check_code(file)