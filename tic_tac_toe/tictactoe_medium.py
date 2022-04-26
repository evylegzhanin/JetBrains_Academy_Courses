def check_win(s):
    list_pos = [[s[0], s[1], s[2]],
            [s[3], s[4], s[5]], 
            [s[6], s[7], s[8]],
            [s[0], s[3], s[6]],
            [s[1], s[4], s[7]],
            [s[2], s[5], s[8]], 
            [s[0], s[4], s[8]], 
            [s[2], s[4], s[6]]]
    flag1 = 0
    flag2 = 0
    for i in range(len(list_pos)):
        new_str = ''.join(list_pos[i])
        if new_str == 'XXX':
          flag1 = 1
        elif new_str == 'OOO':
          flag2 = 1
    if ' ' not in s and (flag1 + flag2) == 0:
        print('Draw')
        return True
    elif flag1 == 1 and flag2 == 0:
        print('X wins')
        return True
    elif flag1 == 0 and flag2 == 1:
        print('X wins')
        return True
    return False


# write your code here
print('-' * 9)
print('| ', ' ' * 5, ' |', '\n', '| ', ' ' * 5, ' |', '\n', '| ', ' ' * 5, ' |', sep='')
print('-' * 9)
check_num = '0123456789'
s = ' ' * 9
process = False
turn = 0
while not process:
    flag = False
    input_move = input('Enter the coordinates:').split()
    while not flag:
        if input_move[0] in check_num and input_move[1] in check_num:
            move = list(map(int, input_move))
            if 0 < move[0] < 4 and 0 < move[1] < 4:
                ind = 3 * (move[0] - 1) + move[1] - 1
                new_s = list(s)
                if new_s[ind] != ' ':
                    print('This cell is occupied! Choose another one!')
                    input_move = input('Enter the coordinates:').split()
                else:
                    flag = True
            else:
                print('Coordinates should be from 1 to 3!')
                input_move = input('Enter the coordinates:').split()
        else:
            print('You should enter numbers!')
            input_move = input('Enter the coordinates:').split()
    if turn % 2 == 0:
        new_s[ind] = 'X'
    else:
        new_s[ind] = 'O'
    m_string = ' '.join(new_s)
    print('-' * 9)
    print('| ', m_string[:5], ' |', '\n', '| ', m_string[6:11], ' |', '\n', '| ', m_string[12:17], ' |', sep='')
    print('-' * 9)
    s = new_s
    process = check_win(s)
