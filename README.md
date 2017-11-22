# CS3251Project2

We ran the code using the following specifications in a Unix environment:
    - python version = 2.7.10
    - numpy version = 1.12.0

High Level Implementation Idea:
	Mitch and I followed the general game flow of hangman for our implementation. In a very high level sense, the implementation idea is below.
	
	1) Start server listening on port X
	2) Start client on IP Y and port X
	3) Server asks client if they are ready to play
	4) Client responds with yes or no (if no, connection is dropped)
	5) Server send over word to guess 
	6) Client guesses one letter at a time
	7) Server responds with the word and guess letters filled in if they were in the word. If they were not in the word, the guessed letter will show in the guessed letters list.
	8) Repeat steps 6 and 7 until the client guesses the full word, or runs out of guesses. If the client finds the word, then they win. If not, they lose.
	9) Drop all connections.

Names of Team Members:

Samuel Alexander Bretz
Mitchell Carlton Myers

Work Division:

We both collaborated on the code implementation, debugging and write up. 

How to run code:

Navigate to main directory:

	(if you don't have numpy installed, then run this)
        To install dependencies:
            make

	To run server (if word dictionary is included, .txt file must be in same directory as server.py):
		python server.py [port num] [optional- word_dictionary file name]
	
	To run client:
		python client.py [IP addr] [port num]
		
Test Results:

(When no word dict is specified, the following is used) -  ['panda', 'snake', 'dog', 'rhino', 'giraffe', 'donkey', 'lion', 'flamingo', 'koala', 'horse',
	             'gorilla', 'buffalo', 'spider', 'mouse', 'eagle']
	
SUCCESFUL CLIENT-

Samuels-MacBook-Pro-2:CS3251Project2 samuel_bretz$ python client.py 127.0.0.1 2018
Ready to start the game? (y/n): y
_ _ _ _ _ _
Incorrect Guesses:
Letter to guess: a


_ _ _ _ _ _
Incorrect Guesses: a
Letter to guess: f


_ _ _ _ _ _
Incorrect Guesses: a f
Letter to guess: m


_ _ _ _ _ _
Incorrect Guesses: a f m
Letter to guess: i


_ _ _ _ _ _
Incorrect Guesses: a f m i
Letter to guess: o


_ o _ _ _ _
Incorrect Guesses: a f m i
Letter to guess: g


_ o _ _ _ _
Incorrect Guesses: a f m i g
Letter to guess: k


_ o _ k _ _
Incorrect Guesses: a f m i g
Letter to guess: d


d o _ k _ _
Incorrect Guesses: a f m i g
Letter to guess: n


d o n k _ _
Incorrect Guesses: a f m i g
Letter to guess: e


d o n k e _
Incorrect Guesses: a f m i g
Letter to guess: y


You won!! The word was: donkey	

UNSUCCESFUL CLIENT-
Samuels-MacBook-Pro-2:CS3251Project2 samuel_bretz$ python client.py 127.0.0.1 2018
Ready to start the game? (y/n): y
_ _ _ _ _ _ _
Incorrect Guesses:
Letter to guess: d


_ _ _ _ _ _ _
Incorrect Guesses: d
Letter to guess: f


_ _ _ _ f f _
Incorrect Guesses: d
Letter to guess: f


Error! Letter f has been guessed before, please guess another letter.

_ _ _ _ f f _
Incorrect Guesses: d
Letter to guess: dsc


Error! Please guess one letter.

Letter to guess: a


_ _ _ a f f _
Incorrect Guesses: d
Letter to guess: 3


Error! Please guess one letter.

Letter to guess: 55


Error! Please guess one letter.

Letter to guess: df


Error! Please guess one letter.

Letter to guess: d


Error! Letter d has been guessed before, please guess another letter.

_ _ _ a f f _
Incorrect Guesses: d
Letter to guess: c


_ _ _ a f f _
Incorrect Guesses: d c
Letter to guess: v


_ _ _ a f f _
Incorrect Guesses: d c v
Letter to guess: a


Error! Letter a has been guessed before, please guess another letter.

_ _ _ a f f _
Incorrect Guesses: d c v
Letter to guess: d


Error! Letter d has been guessed before, please guess another letter.

_ _ _ a f f _
Incorrect Guesses: d c v
Letter to guess: f


Error! Letter f has been guessed before, please guess another letter.

_ _ _ a f f _
Incorrect Guesses: d c v
Letter to guess: g


g _ _ a f f _
Incorrect Guesses: d c v
Letter to guess: v


Error! Letter v has been guessed before, please guess another letter.

g _ _ a f f _
Incorrect Guesses: d c v
Letter to guess: d


Error! Letter d has been guessed before, please guess another letter.

g _ _ a f f _
Incorrect Guesses: d c v
Letter to guess: a


Error! Letter a has been guessed before, please guess another letter.

g _ _ a f f _
Incorrect Guesses: d c v
Letter to guess: e


g _ _ a f f e
Incorrect Guesses: d c v
Letter to guess: r


g _ r a f f e
Incorrect Guesses: d c v
Letter to guess: q


g _ r a f f e
Incorrect Guesses: d c v q
Letter to guess: k


g _ r a f f e
Incorrect Guesses: d c v q k
Letter to guess: m


Game Over!! The word was: giraffe

SERVER OVERLOAD (from client side):
Samuels-MacBook-Pro-2:CS3251Project2 samuel_bretz$ python client.py 127.0.0.1 2018 -y
Ready to start the game? (y/n): y
Server overloaded!

SERVER OVERLOAD (from server side):
Samuels-MacBook-Pro-2:CS3251Project2 samuel_bretz$ python server.py 2018

Get connected from 127.0.0.1 : 59846
Get connected from 127.0.0.1 : 59848
Get connected from 127.0.0.1 : 59849
Get connected from 127.0.0.1 : 59853
End the connection from 127.0.0.1 : 59853

SUCCESSFUL CLIENT/SERVER WITH OPTIONAL WORD DICTIONARY:

Server:
Samuels-MacBook-Pro-2:CS3251Project2 samuel_bretz$ python server.py 2017 word_dict.txt
Get connected from 127.0.0.1 : 59879
End the connection from 127.0.0.1 : 59879

Client:
Samuels-MacBook-Pro-2:CS3251Project2 samuel_bretz$ python client.py 127.0.0.1 2017
Ready to start the game? (y/n): y
_ _ _ _
Incorrect Guesses:
Letter to guess: a


_ _ a _
Incorrect Guesses:
Letter to guess: s


_ _ a _
Incorrect Guesses: s
Letter to guess: k


_ _ a _
Incorrect Guesses: s k
Letter to guess: w


_ _ a _
Incorrect Guesses: s k w
Letter to guess: e


_ _ a _
Incorrect Guesses: s k w e
Letter to guess: r


r _ a r
Incorrect Guesses: s k w e
Letter to guess: e


Error! Letter e has been guessed before, please guess another letter.

r _ a r
Incorrect Guesses: s k w e
Letter to guess: o


You won!! The word was: roar




		
	
