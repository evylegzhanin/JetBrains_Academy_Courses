file = open(input('Enter file name: '), 'r', encoding='utf-8')

blank_line = 0

for i, line in enumerate(file.readlines(), start=1):
    if len(line) > 79:
        print(f'Line {i}: S001 Too Long')

    if (len(line) - len(line.lstrip(' '))) % 4 != 0:
        print(f'Line {i}: S002 Indentation is not a multiple of four')

    if '#' in line and line.split('#')[0].strip().endswith(';'):
        print(f'Line {i}: S003 Unnecessary semicolon')

    if '#' not in line and line.strip().endswith(';'):
        print(f'Line {i}: S003 Unnecessary semicolon')

    if not line.startswith('#') and '#' in line and not line.split('#')[0].endswith('  '):
        print(f'Line {i}: S004 At least two spaces before inline comment required')

    if '#' in line and 'todo' in line.split('#')[1].lower():
        print(f'Line {i}: S005 TODO found')

    if not line.strip():
        blank_line += 1
    else:
        if blank_line > 2:
            print(f'Line {i}: S006 More than two blank lines used before this line')
        blank_line = 0