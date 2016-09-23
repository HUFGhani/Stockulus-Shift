#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import random, randint
#Define the imports
import twitch
from collections import Counter
import pandas as pd
import os

TIME_STEP_LIMIT = 100
NO_MOVE = -1
BUY = 0
SELL = 1
SWITCH = 2
STARTING_BALANCE = 10000

class StockulusShift():
    def __init__(self):
        self.crt_move = NO_MOVE
        self.balance = STARTING_BALANCE
        self.shares = 0
        self.crt_price = None
        self.stock = 0
        self.equitylist = self.get_csv()
        self.n_equities = len(self.equitylist)
        self.price_history = []
        self.stock_history = []
        self.crt_stock = []
        self.moves = 0
        self.get_price()

    def get_csv(self, filedir='Equity_Data/'):
        files = []
        for f in os.listdir(filedir):
            if '.csv' in f:
                files.append(filedir+f)
        files = sorted(files)

        return files

    def get_price(self):
        if self.moves == 0: 
            self.crt_stock = randint(0, self.n_equities-1)
            assert(self.crt_stock>=0 and self.crt_stock <self.n_equities-1)
        try: 
            table = pd.read_csv(self.equitylist[self.crt_stock])
        except Exception as e:
            print self.equitylist[self.crt_stock]

            # stock_price = table['Price']
            # self.crt_price = stock_price[self.moves]

        else:
            stock_price = table['Price']
            self.crt_price = stock_price[self.moves]
            self.price_history.append(stock_price[self.moves])
            self.stock_history.append(self.crt_stock)
            self.crt_price = stock_price[self.moves]

        return 0

    def get_move(self):
        self.crt_move = randint(0, 2)
        return 0

    def push_move(self):


        self.get_price()
        self.moves += 1


        if self.crt_move == BUY:
            print "BUY",
            self.balance -= self.crt_price
            self.shares += 1
        elif self.crt_move == SELL:
            print "SELL",
            if self.shares >= 1:
                self.balance += self.crt_price
                self.shares -= 1
        elif self.crt_move == SWITCH:
            print "SWITCH",
            self.crt_stock = randint(0, self.n_equities-1)
            self.balance += self.crt_price*self.shares
            self.get_price()
            self.shares = 0
        
        print self.balance, self.shares
        return 0


# class Comments():
#     def __init__(self):
#         # import keypresser
#         self.t = twitch.Twitch();
#         # k = keypresser.Keypresser();

#         #Enter your twitch username and oauth-key below, and the app connects to twitch with the details.
#         #Your oauth-key can be generated at http://twitchapps.com/tmi/
#         username = "lz307";
#         key = "oauth:uqxggjb5i1iqd57dickc794iz7rn46";
#         self.t.twitch_connect(username, key);
#         self.count = Counter()

#     #The main loop
#     while True:
#         #Check for new mesasages
#         new_messages = self.t.twitch_receive_messages();

#         if not new_messages:
#             #No new messages...
#             continue
#         else:
#             for message in new_messages:
#                 #Wuhu we got a message. Let's extract some details from it
#                 msg = message['message'].lower()
#                 username = message['username'].lower()

#                 for move in ("buy", "sell", "switch"):
#                     if move in msg:
#                         self.count[move] += 1
#                 #print(username + ": " + msg);


if __name__ == '__main__':
    import time
    game = StockulusShift()
    print game.moves
    step = 0
    while step < TIME_STEP_LIMIT:
        game.get_move()
        game.push_move()
        step += 1
        print step, game.crt_stock
        #time.sleep(1)
    print game.balance
    print len(game.price_history)
    print len(game.stock_history)
    print game.moves
