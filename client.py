import sys
import socket
import struct

server_ip = sys.argv[1]
server_port = sys.argv[2]

try:
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("Error binding to server socket")
    sys.exit()
client_sock.connect((server_ip, int(server_port)))

while True:
    server_msg = client_sock.recv(1024)
    # msg_length = struct.unpack('B', server_msg[0])[0]
    # msg = struct.unpack('{}s'.format(msg_length), server_msg[1:])[0]
    # print(msg)
    # server_msg = client_sock.recv(1024)
    print(server_msg[1:])
    server_msg_flag = server_msg[0]
    if server_msg_flag == '9':
        user_input = raw_input('')
        if not user_input.islower():
            user_input = user_input.lower()
        if user_input != 'y':
            client_sock.close()
            break
        else:
            client_sock.sendall(str(server_msg_flag) + user_input)
    elif server_msg_flag == '1':
        client_sock.close()
        break
    else:
        user_input = raw_input('Letter to guess: ')
        if not user_input.islower():
            user_input = user_input.lower()
        client_sock.sendall('0' + user_input)
