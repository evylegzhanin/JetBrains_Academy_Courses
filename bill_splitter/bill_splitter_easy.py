import random
print('Enter the number of friends joining (including you):')
number_people = int(input())
if number_people <= 0:
    print('No one is joining for the party')
else:
    print('Enter the name of every friend (including you), each on a new line:')
    dict_ = {}
    for i in range(number_people):
        name = input()
        dict_[name] = 0
    print('Enter the total bill value:')
    final_bill = int(input())
    print('Do you want to use the "Who is lucky?" feature? Write Yes/No:')
    lucky = input()
    if lucky == 'Yes':
        lucky_name = random.choice(list(dict_))
        print(f'{lucky_name} is the lucky one!')
        price_everyone = round(final_bill / (number_people - 1), 2)
        for name in dict_:
            dict_[name] = price_everyone
        dict_[lucky_name] = 0
    else:
        print('No one is going to be lucky')
        price_everyone = round(final_bill / number_people, 2)
        for name in dict_:
            dict_[name] = price_everyone
    print(dict_)