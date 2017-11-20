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

ready_ans = raw_input('Ready to start the game? (y/n): ')


if not ready_ans.islower():
    user_input = ready_ans.lower()
if ready_ans != 'y':
    client_sock.close()
else:
    fmt = 'B{}s'.format(len(' '))
    client_struct = struct.pack(fmt, 0, ' ')
    client_sock.sendall(client_struct)

guesses = []

while True:
    server_msg = client_sock.recv(1024)
    msg_flag = struct.unpack('B', server_msg[0])[0]
    if msg_flag is 0:
        word_length = struct.unpack('B', server_msg[1])[0]
        num_inc_guesses = struct.unpack('B', server_msg[2])[0]
        enc_msg = struct.unpack('{}s'.format(word_length * 2), server_msg[3: 3 + (word_length * 2)])[0]
        inc_guesses = struct.unpack('{}s'.format(num_inc_guesses * 2), server_msg[3 + (word_length * 2):])[0]

        print(enc_msg)
        print('Incorrect Guesses: ' + inc_guesses)

        valid_input = False
        user_input = None
        while valid_input is False:
            user_input = raw_input('Letter to guess: ')
            print('\n')
            if len(user_input) > 1 or not user_input.isalpha():
                print("Error! Please guess one letter.\n")
            else:
                valid_input = True
            if not user_input.islower():
                user_input = user_input.lower()
            if user_input in guesses:
                print("Error! Letter " + user_input + " has been guessed before, please guess another letter.\n")
        guesses.append(user_input)
        fmt = 'B{}s'.format(len(user_input))
        client_struct = struct.pack(fmt, len(user_input), user_input)
        client_sock.sendall(client_struct)
    else:
        enc_msg = struct.unpack('{}s'.format(len(server_msg[1:])), server_msg[1:])[0]
        print(enc_msg)
        client_sock.close()
        break
