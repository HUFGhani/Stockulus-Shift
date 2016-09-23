import socket #imports module allowing connection to IRC
import threading #imports module allowing timing functions
import twitch
from random import randint

#sets variables for connection to twitch chat
# bot_owner = 'owner'
# nick1 = 'lz307' 
# channel1 = '#lz307'
# server = 'irc.twitch.tv'
# password = "oauth:uqxggjb5i1iqd57dickc794iz7rn46";


# nicks = ['fyz11', "bot1011", "bot1012"] 
nick = 'fyz11'
channel = '#lz307'
server = 'irc.twitch.tv'
# password = ["oauth:iab80pn9b66e07em8nw4xb33tg9xrr", 
# "oauth:px0ftogew0f5pqg3soj3okruokw3nu",
# "oauth:yrhteoof3s7vy0jj4mnwhnqzu5ftl3"]
password = "oauth:iab80pn9b66e07em8nw4xb33tg9xrr"
# queue = 13 #sets variable for anti-spam queue functionality

irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, 6667)) #connects to the server
# irc.settimeout(0.6);

queue = 0
def message(msg): #function for sending messages to the IRC chat
	global queue
	queue = queue + 1
	print queue
	if queue < 20: #ensures does not send >20 msgs per 30 seconds.
		irc.send('PRIVMSG ' + channel + ' :' + msg + '\r\n')
	else:
		print 'Message deleted'

def queuetimer(): #function for resetting the queue every 30 seconds
	global queue
	print 'queue reset'
	queue = 0
	threading.Timer(30,queuetimer).start()
	queuetimer()

moves = ["BUY", "SELL", "SWITCH"]

import time
# nick = 'fyz11' 
# channel = '#lz307'
# server = 'irc.twitch.tv'
# password = "oauth:iab80pn9b66e07em8nw4xb33tg9xrr";

# irc.send('PASS ' + password + '\r\n')
# irc.send('USER ' + nick + ' 0 * :' + bot_owner + '\r\n')
# irc.send('NICK ' + nick + '\r\n')
# irc.send('JOIN ' + channel + '\r\n')

# t = twitch.Twitch();
# t.twitch_connect(nick, password);


# t.twitch_send_messages('fdsafsa', channel)
# count = 0
# sends variables for connection to twitch chat

# def bot(passwd, nick)
irc.send('PASS ' + password + '\r\n')
irc.send('USER ' + nick + '\r\n')
irc.send('NICK ' + nick + '\r\n')
irc.send('JOIN ' + channel + '\r\n')

for i in range(5):

	# for i in range(len(nicks)):
		# irc.sendall('PRIVMSG ' + channel+' :hi my name is neo')

		# irc.send('PASS ' + password + '\r\n')
		# irc.send('USER ' + nick + '\r\n')
		# irc.send('NICK ' + nick + '\r\n')
		# irc.send('JOIN ' + channel + '\r\n')
		
		# babadata = irc.recv(1204) #gets output from IRC server
		# babauser = babadata.split(':')[1]
		# babauser = babauser.split('!')[0] #determines the sender of the messages
		# print babadata

		# irc.sendall('PRIVMSG ' + channel +' :hi my name is neo')
	msg = moves[randint(0, len(moves)-1)]
	# nick = nicks[i]
	# passwd = password[i]
	# irc.send('PRIVMSG #lz307 :'+str(msg)+'\r\n')
	# time.sleep(0.5)

	data = irc.recv(1204) #gets output from IRC server
	user = data.split(':')[1]
	user = user.split('!')[0] #determines the sender of the messages

	# if data.find('PING') != -1:
		# irc.send(data.replace('PING', 'PONG')) #responds to PINGS from the server
	# if data.find('!test') != -1: #!test command
	message(msg)

		# if irc.recv(1204):
			# continue
		# irc.sendall('hi my name is neo')

		# if babadata.find('PING') != -1:
		#     irc.send(babadata.replace('PING', 'PONG')) #responds to PINGS from the server
