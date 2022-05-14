# write your code here
import sys
import socket
import itertools
import string

args = sys.argv
if len(args) != 3:
    print("The script should be called with 2 arguments (IP and port)")
else:
    ip = args[1]
    port = int(args[2])


def find_password(socket_cl, mode='bruteforce'):
    if mode == 'bruteforce':
        alpha_num_list =  list(string.ascii_lowercase + string.digits)
        i = 1
        counter = 1
        while counter <= 1e6:
            for iteration in itertools.product(alpha_num_list, repeat=i):
                joined_iter = ''.join(iteration)
                data_to_send = joined_iter.encode()
                socket_cl.send(data_to_send)
                response_form_ser = socket_cl.recv(1024)
                # decoding from bytes to string
                response_form_ser = response_form_ser.decode()
                if response_form_ser == 'Connection success!':
                    return joined_iter
                counter += 1
            i += 1


# creating a client socket
with socket.socket() as client_socket:
    address = (ip, port)
    client_socket.connect(address)
    print(find_password(client_socket))