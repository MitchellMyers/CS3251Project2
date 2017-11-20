import socket
import sys
from thread import *
import numpy as np
import struct

port_num = sys.argv[1]
# words_file = open(sys.argv[1], 'r') if sys.argv[1] is not None else None
word_dict = ['panda', 'snake', 'dog', 'chimpanzee', 'giraffe', 'donkey', 'lion', 'flamingo', 'koala', 'horse',
             'gorilla', 'caterpillar', 'spider', 'mouse', 'eagle']


def decode_word(word, enc_word, letter):
    dec_word_list = list(enc_word)
    for i in range(len(word)):
        if word[i] is letter:
            dec_word_list[i * 2] = letter
    return ''.join(dec_word_list)


def encode_word(word):
    enc_word_list = list(word)
    for i in range(len(word)):
        enc_word_list[i] = '_'
    return ''.join(enc_word_list)

# def packetize(msg):
#     msg_len = len(msg)
#     return struct.pack('B{}s'.format(msg_len), msg_len, msg)



server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    server_sock.bind(('localhost', int(port_num)))
except socket.error:
    print("Error binding to server socket")
    sys.exit()

server_sock.listen(10)

def thread(client_connect):
    word = np.random.choice(word_dict, 1)[0]
    print('\n' + word)

    enc_word = []
    for i in range(len(word)):
        enc_word.append('_ ')
    enc_word = ''.join(enc_word)



    start_msg = 'Ready to start the game? (y/n): '
    # start_msg_flag = chr(9)
    # start_msg_ascii = start_msg_flag + start_msg

    fmt = 'B{}s'.format(len(start_msg))
    victory_struct = struct.pack(fmt, 9, start_msg)

    client_connect.sendall(victory_struct)

    inc_guesses = []
    cor_guesses = []
    cor_count = 0
    while True:
        client_msg = client_connect.recv(1024)
        client_msg_flag = struct.unpack('B', client_msg[0])[0]
        if client_msg_flag is 9:
            resp = struct.unpack('{}s'.format(1), client_msg[1])[0]
            if resp == 'n':
                client_connect.close()
            elif resp == 'y':
                fmt = 'BBB{}s{}s'.format(len(enc_word), len(inc_guesses * 2))
                struct_con = struct.pack(fmt, 0, len(word), len(inc_guesses), enc_word, '')
                client_connect.sendall(struct_con)
        else:
            guessed_letter = client_msg[1]
            curr_enc_word = decode_word(word, enc_word, guessed_letter)
            if guessed_letter not in word and (guessed_letter + ' ') not in inc_guesses:
                inc_guesses.append(guessed_letter + ' ')
            elif guessed_letter in word and guessed_letter not in cor_guesses:
                cor_guesses.append(guessed_letter)
                cor_count += word.count(guessed_letter)
            if len(inc_guesses) > 5:
                game_over_msg = 'Game Over!! The word was: ' + word
                fmt = 'B{}s'.format(len(game_over_msg))
                game_over_struct = struct.pack(fmt, len(game_over_msg), game_over_msg)
                client_connect.sendall(game_over_struct)
                break
            if cor_count is len(word):
                victory_msg = 'You won!! The word was: ' + word
                fmt = 'B{}s'.format(len(victory_msg))
                victory_struct = struct.pack(fmt, len(victory_msg), victory_msg)
                client_connect.sendall(victory_struct)
                break
            fmt = 'BBB{}s{}s'.format(len(curr_enc_word), len(inc_guesses * 2))
            struct_con = struct.pack(fmt, 0, len(word), len(inc_guesses), curr_enc_word, ''.join(inc_guesses))
            client_connect.sendall(struct_con)
            enc_word = curr_enc_word


    client_connect.close()


num_clients = 0
while True:
    client_conn, addr = server_sock.accept()
    if client_conn and addr:
        num_clients += 1
    start_new_thread(thread, (client_conn,))
    print("Get connected from {} : {}".format(addr[0], str(addr[1])))
    if num_clients > 3:
        break

server_sock.close()
