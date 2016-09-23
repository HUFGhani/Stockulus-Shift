#!/usr/bin/env python
# -*- coding: utf-8 -*-
from random import random, randint
#Define the imports
import twitch
from collections import Counter
import threading
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
        self.comments = Comments()

        self.equitylist = self.get_csv()
        self.n_equities = len(self.equitylist)
        self.price_history = []
        self.stock_history = []
        self.crt_stock = []
        self.moves = 0
        self.get_price()

    def get_csv(self, filedir='Data/'):
        files = []
        for f in os.listdir(filedir):
            if '.txt' in f:
                files.append(filedir+f)
        files = sorted(files)

        return files

    def release(self):
        self.comments.release()

    def get_price(self):
        table = {'Price': []}
        if self.moves == 0:
            self.crt_stock = randint(0, self.n_equities-1)
            assert(self.crt_stock>=0 and self.crt_stock <self.n_equities)
        try:

            with open(self.equitylist[self.crt_stock], 'r') as f:
                for line in f:
                    table = pd.read_csv(self.equitylist[self.crt_stock])
        except Exception as e:
            print self.equitylist[self.crt_stock]

        else:
            stock_price = table['Price']
            self.crt_price = stock_price[self.moves]
            self.price_history.append(stock_price[self.moves])
            self.stock_history.append(self.crt_stock)
            self.crt_price = stock_price[self.moves]

        return 0

    def get_move(self):
        self.crt_move = self.comments.get_move()
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
            self.crt_stock = randint(0, 5)
            self.balance += self.crt_price*self.shares
            self.get_price()
            self.shares = 0
        print self.balance, self.shares, self.crt_price
        return 0

    def update(self):
        self.get_move()
        self.push_move()

class Comments():
    def __init__(self):
        # import keypresser
        self.t = twitch.Twitch();
        # k = keypresser.Keypresser();

        #Enter your twitch username and oauth-key below, and the app connects to twitch with the details.
        #Your oauth-key can be generated at http://twitchapps.com/tmi/
        username = "sentimentron"
        key = "oauth:2upqjc2h4vzy1qlpuiq27l9evewpye"
        self.t.twitch_connect(username, key)
        self.count = Counter()
        self.lock = threading.Lock()
        self.moves = ("buy", "sell", "switch")
        self.stop = False

        def update():
            #The main loop
            while not self.stop:
                time.sleep(5)
                print 'getting comments'
                #Check for new mesasages

                new_messages = self.t.twitch_receive_messages();
                print "MSG", new_messages

                if not new_messages:
                    #No new messages...
                    continue
                else:
                    for message in new_messages:
                        print "MSG_", message
                        #Wuhu we got a message. Let's extract some details from it
                        msg = message['message'].lower()
                        #username = message['username'].lower()
                        print msg

                        with self.lock:
                            for move in self.moves:
                                if move in msg:
                                    self.count[move] += 1

                        #print(username + ": " + msg);

        self.thread = threading.Thread(target=update)
        self.thread.start()

    def release(self):
        print 'stopping thread'
        self.stop = True

    def get_move(self):
        with self.lock:
            results = self.count.most_common(1)
            print self.count
            if len(results) >= 1:
                action, count = results[0]
                for i in self.count.keys():
                    self.count.pop(i, None)
                return action.upper()
            return "NO_ACTION"
            li = [ self.count[x] for x in self.count ]
            if len(li) == 0:
                return "NO_MOVE"
            i = li.index(max(li))
            for move in self.moves:
                self.count[move] = 0

            return ["BUY", "SELL", "SWITCH"][i]



if __name__ == '__main__':
    import time
    # game = StockulusShift()
    # step = 0
    # while step < TIME_STEP_LIMIT:
    #     game.update()
    #     step += 1
    #     print step,
    #     #time.sleep(1)
    # print game.balance
    # game.release()
    c = Comments()
    i = 0
    try:
        while True:
            with open('action','w') as fd:
                fd.write(c.get_move())
            time.sleep(5)
    except Exception, e:
        raise
    finally:
        c.release
