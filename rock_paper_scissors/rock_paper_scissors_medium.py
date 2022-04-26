# Write your code here
import random

name = input('Enter your name: ')
print('Hello,', name)
rating_file = open('rating.txt')
score = 0

for line in rating_file:
    if line.split()[0] == name:
        score = int(line.split()[1])
rating_file.close()
input_list = input().split(',')
print("Okay, let's start")
dct = {}

if input_list == ['']:
    list_options = ['rock', 'scissors', 'paper']
    dct = {'rock': 'scissors', 'scissors': 'paper', 'paper': 'rock'}
else:
    list_options = list(input_list)
    for word in input_list:
        new_list = input_list[input_list.index(word) + 1:]
        new_list.extend(input_list[:input_list.index(word)])
        dct_list = []
        dct_list.extend(new_list[(len(new_list) // 2):])
        dct[word] = dct_list
list_options.append('!rating')
choice = input()

while choice in list_options:
    computer_choice = random.choice(list_options[:-1])
    if choice == computer_choice:
        score += 50
        print(f'There is a draw ({choice})')
    elif choice == '!rating':
        print('Your rating:', score)
    elif computer_choice in dct.get(choice):
        print(f'Well done. The computer chose {computer_choice} and failed')
        score += 100
    else:
        print(f'Sorry, but the computer chose {computer_choice}')
    choice = input()

if choice == '!exit':
    print('Bye!')
else:
    print('Invalid input')
