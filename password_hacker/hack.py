# write your code here
import sys
import socket

args = sys.argv
if len(args) != 4:
    print("The script should be called with 3 arguments (IP, port and message)")
else:
    ip = args[1]
    port = int(args[2])
    message = args[3]

# creating a client socket
with socket.socket() as client_socket:
    address = (ip, port)
    client_socket.connect(address)
    data = message.encode()
    client_socket.send(data)
    response = client_socket.recv(1024)
    # decoding from bytes to string
    response = response.decode()
    print(response)