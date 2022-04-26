# Write your code here
from copy import deepcopy


def board_creation():
    while True:
        try:
            x, y = map(int, input('Enter your board dimensions: ').split())
            if x <= 0 or y <= 0:
                print('Invalid dimensions!')
            else:
                break
        except ValueError:
            print('Invalid dimensions!')
    list_field = []
    for i in range(y):
        list_str = ['_' * len(str(x * y))] * x
        list_field.append(list_str)
    return x, y, list_field


def design_field(field_for_design, x, y):
    boarder_line = x * (len(str(x * y)) + 1) + 3
    print(' ', '-' * boarder_line, sep='')
    for i in range(y, 0, - 1):
        print(str(i), '| ', ' '.join(field_for_design[i - 1]), ' |', sep='')
    print(' ', '-' * boarder_line, sep='')
    str_num = ''
    for i in range(x):
        str_num += ' ' * (len(str(x * y)))
        str_num += str(i + 1)
    print(' ', str_num, ' ')


def first_move(x, y, field):
    while True:
        move_str = input("Enter the knight's starting position: ")
        try:
            move = list(map(int, move_str.split()))
            if len(move) != 2:
                print('Invalid position!')
            else:
                if 0 < move[0] < (x + 1) and 0 < move[1] < (y + 1):
                    break
                else:
                    print('Invalid position!')
        except ValueError:
            print('Invalid position!')

    first_move_field = deepcopy(field)
    first_move_field[move[1] - 1][move[0] - 1] = ' ' * (cell_size - 1) + 'X'

    return move, first_move_field


def check_next_move(x, y, list_of_options):
    while True:
        move_str = input("Enter your next move: ")
        try:
            move = list(map(int, move_str.split()))
            if len(move) != 2:
                print('Invalid move!', end='')
            else:
                list_conditions = [0 < move[0] < (x + 1), 0 < move[1] < (y + 1),
                                   move in list_of_options]
                if all(list_conditions):
                    break
                else:
                    print('Invalid move!', end='')
        except ValueError:
            print('Invalid move!', end='')
    return move


def make_next_move(init_field, move, previous_move, cell_size):
    field = deepcopy(init_field)
    field[previous_move[1] - 1][previous_move[0] - 1] = ' ' * (cell_size - 1) + '*'
    field[move[1] - 1][move[0] - 1] = ' ' * (cell_size - 1) + 'X'
    return field


def solution_next_move(init_field, move, cell_size, counter):
    field = deepcopy(init_field)
    num_digits = len(str(counter))
    field[move[1] - 1][move[0] - 1] = ' ' * (cell_size - num_digits) + str(counter)
    return field


def make_possible_move(initial_field, move, list_old_pos, cell_size, number_of_options=0):
    field = deepcopy(initial_field)
    if move not in list_old_pos:
        field[move[1] - 1][move[0] - 1] = ' ' * (cell_size - 1) + str(number_of_options)
    return field


def count_options(tmp_pos, list_old_pos, x, y):
    list_moves = [[-2, -1], [-2, 1], [-1, 2], [-1, -2], [1, 2], [1, -2], [2, -1], [2, 1]]
    count = 0
    for i in range(8):
        x_tmp = tmp_pos[0] - list_moves[i][0]
        y_tmp = tmp_pos[1] - list_moves[i][1]
        if 0 < x_tmp < (x + 1) and 0 < y_tmp < (y + 1):
            if [x_tmp, y_tmp] not in list_old_pos:
                count += 1
    return count


def possible_moves(field, position, list_old_pos, x, y, cell_size):
    list_moves = [[-2, -1], [-2, 1], [-1, 2], [-1, -2], [1, 2], [1, -2], [2, -1], [2, 1]]
    counter = 0
    opt_list = []
    best_move = []
    best_option_num = 9
    number_of_options = 0
    for i in range(8):
        x_tmp = position[0] - list_moves[i][0]
        y_tmp = position[1] - list_moves[i][1]
        list_cond = [0 < x_tmp < (x + 1), 0 < y_tmp < (y + 1), [x_tmp, y_tmp] not in list_old_pos]
        if all(list_cond):
            move_tmp = [x_tmp, y_tmp]
            number_of_options = count_options(move_tmp, list_old_pos, x, y)
            if number_of_options <= best_option_num:
                best_option_num = number_of_options
                best_move = move_tmp
            field = make_possible_move(field, move_tmp, list_old_pos, cell_size, number_of_options)
            counter += 1
            opt_list.append(move_tmp)

    return field, opt_list, best_move


def play_the_game(x, y, base_field_copy, field_first_move, move, cell_size):
    list_old_pos = []
    counter_moves = 1
    while True:
        list_old_pos.append(move)
        field, list_of_options, best_move = possible_moves(field_first_move, move, list_old_pos, x, y, cell_size)
        if not list_of_options:
            if counter_moves != x * y:
                print('No more possible moves!')
                print(f'Your knight visited {counter_moves} squares!')
                break
            else:
                print('What a great tour! Congratulations!')
                break
        design_field(field, x, y)
        previous_move = move
        move = check_next_move(x, y, list_of_options)
        base_field_copy = make_next_move(base_field_copy, move, previous_move, cell_size)
        field_first_move = deepcopy(base_field_copy)
        counter_moves += 1


def check_solutions(x, y, base_field_copy, field_first_move, move, cell_size):
    list_old_pos = []
    counter_moves = 1
    while True:
        list_old_pos.append(move)
        field, list_of_options, best_move = possible_moves(field_first_move, move, list_old_pos, x, y, cell_size)
        list_of_options = [item for item in list_of_options if item not in list_old_pos]
        previous_move = move
        if not list_of_options:
            if counter_moves != x * y:
                flag = False
                break
            else:
                flag = True
                break
        move = best_move
        base_field_copy = make_next_move(base_field_copy, move, previous_move, cell_size)
        field_first_move = deepcopy(base_field_copy)
        counter_moves += 1
    return flag


def show_solution(x, y, base_field_copy, move, cell_size):
    list_old_pos = [move]
    counter_moves = 1
    num_digits = len(str(counter_moves))
    base_field_copy[move[1] - 1][move[0] - 1] = ' ' * (cell_size - num_digits) + str(counter_moves)
    while True:
        field, list_of_options, best_move = possible_moves(base_field_copy, move, list_old_pos, x, y, cell_size)
        list_of_options = [item for item in list_of_options if item not in list_old_pos]
        base_field_copy = solution_next_move(base_field_copy, move, cell_size, counter_moves)
        if not list_of_options:
            break
        move = best_move
        list_old_pos.append(move)
        counter_moves += 1
    return base_field_copy


x, y, base_field = board_creation()
move, field_first_move = first_move(x, y, base_field)
cell_size = len(str(x * y))

while True:
    answer = input('Do you want to try the puzzle? (y/n): ')
    if answer == 'y':
        flag = check_solutions(x, y, base_field, field_first_move, move, cell_size)
        if not flag:
            print('No solution exists!')
            break
        else:
            play_the_game(x, y, base_field, field_first_move, move, cell_size)
            break
    elif answer == 'n':
        flag = check_solutions(x, y, base_field, field_first_move, move, cell_size)
        if not flag:
            print('No solution exists!')
            break
        else:
            field_solution = show_solution(x, y, base_field, move, cell_size)
            print("Here's the solution!")
            design_field(field_solution, x, y)
            break
    else:
        print('Invalid input!', end='')

