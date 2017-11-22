import sys
import socket
import struct

# Pull out the server IP and Port from the command line arguments
server_ip = sys.argv[1]
server_port = sys.argv[2]

# Create a new client socket
try:
    client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print("Error binding to server socket")
    sys.exit()

# Connect to the server IP address and port
client_sock.connect((server_ip, int(server_port)))

# Ask if user is ready to start the game
ready_ans = raw_input('Ready to start the game? (y/n): ')

# Reformat the user's answer and if it is not a y (or Y) then close the socket
if not ready_ans.islower():
    user_input = ready_ans.lower()
if ready_ans != 'y':
    client_sock.close()
# If user ready to play, then send an empty packet with msg_flag set to 0 to signal to the server to send an
# encoded word
else:
    fmt = 'B{}s'.format(len(' '))
    client_struct = struct.pack(fmt, 0, ' ')
    client_sock.sendall(client_struct)

guesses = []

while True:
    # Receive a message from the server
    server_msg = client_sock.recv(1024)
    # Unpack the msg_flag to differentiate between a control packet and a non-control packet
    msg_flag = struct.unpack('B', server_msg[0])[0]
    # If it's a control packet, then unpack the word length, num incorrect guesses, encoded word, and incorrect guesses
    if msg_flag is 0:
        word_length = struct.unpack('B', server_msg[1])[0]
        num_inc_guesses = struct.unpack('B', server_msg[2])[0]
        enc_msg = struct.unpack('{}s'.format(word_length * 2), server_msg[3: 3 + (word_length * 2)])[0]
        inc_guesses = struct.unpack('{}s'.format(num_inc_guesses * 2), server_msg[3 + (word_length * 2):])[0]

        # Print the current encoded word
        print(enc_msg)
        # Print all of the incorrect guesses by the user thus far
        print('Incorrect Guesses: ' + inc_guesses)

        valid_input = False
        user_input = None
        # Check if the letter guessed by the user fits the criteria (i.e. is only one letter)
        # If false, then prompt the user to guess again and again until they input a valid answer
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
        # Keep track of the guesses to make sure the user doesn't guess the same letter again
        guesses.append(user_input)
        # Pack the guessed letter into a struct and send it to the client
        fmt = 'B{}s'.format(len(user_input))
        client_struct = struct.pack(fmt, len(user_input), user_input)
        client_sock.sendall(client_struct)
    # The server has sent a game ending packet which means the user either guessed the correct answer, or the user
    # used up all guesses and it's game over. Print out the message and close the client socket
    else:
        enc_msg = struct.unpack('{}s'.format(len(server_msg[1:])), server_msg[1:])[0]
        print(enc_msg)
        client_sock.close()
        break
