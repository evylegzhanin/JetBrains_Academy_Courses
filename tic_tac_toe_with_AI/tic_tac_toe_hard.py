# write your code here
import random
import sys
import time

sys.setrecursionlimit(100)


def design_field(state):
    print('-' * 9)
    for i in range(3):
        print('| ', ' '.join(state[i * 3:i * 3 + 3]), ' |', sep='')
    print('-' * 9)


def make_move(cur_state):
    state = cur_state.copy()
    while True:
        try:
            move_tmp = list(map(int, input('Enter the coordinates: ').split()))
        except ValueError:
            print('You should enter numbers!')
        else:
            if len(move_tmp) == 2:
                if 0 < move_tmp[0] < 4 and 0 < move_tmp[1] < 4:
                    position = (move_tmp[0] - 1) * 3 + move_tmp[1] - 1
                    if state[position] == ' ':
                        if state.count('X') == state.count('O'):
                            turn = 'X'
                        else:
                            turn = 'O'
                        state[position] = turn
                        break
                    else:
                        print('This cell is occupied! Choose another one!')
                else:
                    print('Coordinates should be from 1 to 3!')
            else:
                print('There should be 2 coordinates!')
    return state


def who_wins(cur_state, show):
    list_pos = [[cur_state[0], cur_state[1], cur_state[2]],
                [cur_state[3], cur_state[4], cur_state[5]],
                [cur_state[6], cur_state[7], cur_state[8]],
                [cur_state[0], cur_state[3], cur_state[6]],
                [cur_state[1], cur_state[4], cur_state[7]],
                [cur_state[2], cur_state[5], cur_state[8]],
                [cur_state[0], cur_state[4], cur_state[8]],
                [cur_state[2], cur_state[4], cur_state[6]]]
    flag1 = 0
    flag2 = 0
    for i in range(len(list_pos)):
        new_str = ''.join(list_pos[i])
        if new_str == 'XXX':
            flag1 = 1
        elif new_str == 'OOO':
            flag2 = 1
    if (flag1 + flag2) == 0:
        if ' ' not in cur_state:
            if show:
                print('Draw')
            return False, 0
        else:
            return True, 'Continue'
    elif flag1 == 1 and flag2 == 0:
        if show:
            print('X wins')
        return False, 'X'
    elif flag1 == 0 and flag2 == 1:
        if show:
            print('O wins')
        return False, 'O'


def get_winner(cur_state, sign):
    state = cur_state.copy()
    flag, winner = who_wins(state, False)
    if winner == 0:
        result = 0
    elif winner == sign:
        result = 1
    elif winner == 'Continue':
        result = None
    else:
        result = -1
    return result


def change_sign(sign):
    if sign == 'X':
        tmp_sign = 'O'
    else:
        tmp_sign = 'X'
    return tmp_sign


def minimax_algorithm(cur_state, sign, player, depth):
    state = cur_state.copy()
    if get_winner(state, player) is not None:
        return get_winner(state, player)
    else:
        list_of_options = []
        for i in range(len(state)):
            if state[i] == ' ':
                list_of_options.append(i)
        value_result = []
        sign = change_sign(sign)
        for k in list_of_options:
            tmp_state = state.copy()
            tmp_state[k] = sign
            result = minimax_algorithm(tmp_state, sign, player, depth + 1)
            value_result.append(result)
        if depth % 2 == 0:
            best_choice = max(value_result)
        else:
            best_choice = min(value_result)
        return best_choice


def automatic_move(cur_state, level):
    state = cur_state.copy()
    if state.count('X') == state.count('O'):
        sign = 'X'
    else:
        sign = 'O'
    player = sign
    list_of_options = []
    for i in range(len(cur_state)):
        if cur_state[i] == ' ':
            list_of_options.append(i)

    if level == 'easy':
        print('Making move level "easy"')
        index_of_the_move = random.choice(list_of_options)

    elif level == 'medium':
        print('Making move level "medium"')
        show = False
        top_move = -1
        for i in list_of_options:
            tmp_state = cur_state.copy()
            tmp_state[i] = 'X'
            flag, winner = who_wins(tmp_state, show)
            if not flag:
                top_move = i
        if top_move != -1:
            index_of_the_move = top_move
        else:
            index_of_the_move = random.choice(list_of_options)

    elif level == 'hard':
        print('Making move level "hard"')
        depth = 0
        best_score = -100
        index_of_the_move = None
        for i in list_of_options:
            tmp_state = state.copy()
            tmp_state[i] = sign
            score = minimax_algorithm(tmp_state, sign, player, depth + 1)
            # print(score)
            if score > best_score:
                best_score = score
                index_of_the_move = i
    state[index_of_the_move] = sign
    return state


def choose_move(cur_state, who):
    state = cur_state.copy()
    opt_ai = ['easy', 'medium', 'hard']
    if who == 'user':
        state = make_move(state)
    elif who in opt_ai:
        state = automatic_move(state, who)
    return state


def play_game(cur_state, player1, player2):
    state = cur_state.copy()
    loop_active = True
    design_field(initial_state)
    show = True
    while loop_active:
        state = choose_move(state, player1)
        design_field(state)
        loop_active, winner = who_wins(state, show)
        if not loop_active:
            break
        state = choose_move(state, player2)
        design_field(state)
        loop_active, winner = who_wins(state, show)


while True:
    empty_field = '_________'
    empty_field = empty_field.replace('_', ' ')
    initial_state = list(empty_field)
    now_state = initial_state.copy()
    command = input('Input command: ').split()
    list_opt_1 = ['exit', 'start']
    list_opt_2 = ['easy', 'medium', 'hard', 'user']
    if len(command) == 3:
        list_cond = [command[0] in list_opt_1,
                     command[1] in list_opt_2,
                     command[2] in list_opt_2]
        if all(list_cond):
            play_game(now_state, command[1], command[2])
        else:
            print('Bad parameters!')
    elif len(command) == 1 and command[0] == 'exit':
        break
    else:
        print('Bad parameters!')


