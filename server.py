import socket
import sys
from thread import *
import numpy as np
import struct

# Pulling out the port number from the command line argument
port_num = sys.argv[1]
word_dict = []

# Process to populate the word dictionary list if a file with words is given as a command line arg
try:
	# Check if argument is there
	file_name = sys.argv[2]

	# Perform I/O
	f = open(str(file_name), "r")
	content_list = []
	for line in f:
		content_list.append(line.strip('\n'))
	content_list[:] = [i for i in content_list if i != '']

	# Populate word dict
	for i in range(1,len(content_list)):
		word_dict.append(content_list[i])
except:
	word_dict = ['panda', 'snake', 'dog', 'rhino', 'giraffe', 'donkey', 'lion', 'flamingo', 'koala', 'horse',
	             'gorilla', 'buffalo', 'spider', 'mouse', 'eagle']

# Helper function that takes in the current encoded word and puts the letter in the correct spot if its in the word
def decode_word(word, enc_word, letter):
    # Change the string into a list for ease of mutability
    dec_word_list = list(enc_word)
    for i in range(len(word)):
        # Checks if the current letter is the guessed letter
        if word[i] is letter:
            # If so, then change the letter's spot in the encoded word from '_' to the guessed letter
            dec_word_list[i * 2] = letter
    # Since a list of characters is used for the decoded word, this joins all of the characters into a string
    return ''.join(dec_word_list)


# Initialize the server socket
server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    # Bind to the socket port
    server_sock.bind(('localhost', int(port_num)))
except socket.error:
    print("Error binding to server socket")
    sys.exit()

# Begin listening for incoming connections from clients
server_sock.listen(10)
num_clients = 0

# Helper method to create new threads to support multiple clients at the same time
def thread(client_connect, addr):
    global num_clients

    # Chooses a random word from the word dictionary list
    word = np.random.choice(word_dict, 1)[0]

    # Encodes the intial word into a series of '_' characters
    # Uses a list for mutability purposes and then converts the list into a string
    enc_word = []
    for i in range(len(word)):
        enc_word.append('_ ')
    enc_word = ''.join(enc_word)

    inc_guesses = []
    cor_guesses = []
    cor_count = 0
    while True:

        # Receive the message from the client
        client_msg = client_connect.recv(1024)
        # Try to unpack. if exception, this means server overload. -> break
        try:
            client_msg_flag = struct.unpack('B', client_msg[0])[0]
        except:
            break

        # Unpack the guessed letter from the client
        guessed_letter = struct.unpack('{}s'.format(1), client_msg[1])[0]
        # Check if it's a control packet, if so, then send the initial control packet with the completely encoded word
        if client_msg_flag is 0:
            # Format the control packet so that it's
            # [flag | word_length | num_incorrect_guesses | encoded_word | inc_guesses]
            fmt = 'BBB{}s{}s'.format(len(enc_word), len(inc_guesses * 2))
            struct_con = struct.pack(fmt, 0, len(word), len(inc_guesses), enc_word, '')
            client_connect.sendall(struct_con)
        else:
            # Decode the word based on the letter guessed
            curr_enc_word = decode_word(word, enc_word, guessed_letter)
            # Check if the letter is not in the word and add it to the incorrect guesses if it is not already in there
            if guessed_letter not in word and (guessed_letter + ' ') not in inc_guesses:
                inc_guesses.append(guessed_letter + ' ')
            # Check if the guessed letter is in the word and if so then add it to the correct guesses
            elif guessed_letter in word and guessed_letter not in cor_guesses:
                cor_guesses.append(guessed_letter)
                cor_count += word.count(guessed_letter)
            # If the user guessed wrong and it's the sixth incorrect guess then the user loses and it's game over
            # Send the game over packet and break out of the loop to close the client connection
            if len(inc_guesses) > 5:
                game_over_msg = 'Game Over!! The word was: ' + word
                fmt = 'B{}s'.format(len(game_over_msg))
                game_over_struct = struct.pack(fmt, len(game_over_msg), game_over_msg)
                client_connect.sendall(game_over_struct)
                break
            # If the user guesses the last un-guessed letter correctly, then the user wins and the game is over
            # Send the victory message packet and break out of the loop to close the client connection
            if cor_count is len(word):
                victory_msg = 'You won!! The word was: ' + word
                fmt = 'B{}s'.format(len(victory_msg))
                victory_struct = struct.pack(fmt, len(victory_msg), victory_msg)
                client_connect.sendall(victory_struct)
                break
            # Send the new decoded word in the newly updated control packet back to the client
            fmt = 'BBB{}s{}s'.format(len(curr_enc_word), len(inc_guesses * 2))
            struct_con = struct.pack(fmt, 0, len(word), len(inc_guesses), curr_enc_word, ''.join(inc_guesses))
            client_connect.sendall(struct_con)
            enc_word = curr_enc_word
    # The client connection is closing so decrement the number of active clients
    num_clients -= 1
    print("End the connection from {} : {}".format(addr[0], str(addr[1])))
    # End the connection to the client
    client_connect.close()

while True:
    # Accept a new client connection
    client_conn, addr = server_sock.accept()

    # Server is overloaded
    if client_conn and addr and num_clients is 3:
        serv_overload = 'Server overloaded!'
        so_struct_fmt = 'B{}s'.format(len(serv_overload))
        so_struct = struct.pack(so_struct_fmt, len(serv_overload), serv_overload)
        client_conn.sendall(so_struct)

    # Allow new client to connect and play
    if client_conn and addr:
        num_clients += 1
        print("Get connected from {} : {}".format(addr[0], str(addr[1])))
        start_new_thread(thread, (client_conn, addr))

