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

def packetize(msg):
    msg_len = len(msg)
    return struct.pack('B{}s'.format(msg_len), msg_len, msg)



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

    # start_msg = 'Ready to start the game? (y/n): '
    # reply_struct = packetize(start_msg)
    client_connect.sendall('9Ready to start the game? (y/n): ')

    inc_guesses = []
    cor_guesses = []
    cor_count = 0
    while True:
        client_msg = client_connect.recv(1024)
        client_msg_flag = client_msg[0]
        if client_msg_flag is '9' and client_msg[1] is 'n':
            client_connect.close()
        elif client_msg_flag is '9' and client_msg[1] is 'y':
            client_connect.sendall('0' + enc_word + '\nIncorrect Guesses: '
                                   + ''.join(inc_guesses) + '\n')
        elif client_msg_flag is '0':
            guessed_letter = client_msg[1]
            curr_enc_word = decode_word(word, enc_word, guessed_letter)
            if guessed_letter not in word and (guessed_letter + ' ') not in inc_guesses:
                inc_guesses.append(guessed_letter + ' ')
            elif guessed_letter in word and guessed_letter not in cor_guesses:
                cor_guesses.append(guessed_letter)
                cor_count += word.count(guessed_letter)
            if len(inc_guesses) > 5:
                client_connect.sendall('1Game Over!! The word was: ' + word)
                break
            if cor_count is len(word):
                client_connect.sendall('1You won!! The word was: ' + word)
                break
            client_connect.sendall('0' + curr_enc_word + '\nIncorrect Guesses: ' + ''.join(inc_guesses) + '\n')
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
