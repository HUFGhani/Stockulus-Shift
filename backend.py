import os
import time
import random

def path_leaf(path):
    filename = path.split("/")
    root,_,_ = filename[-1].partition('.')
    return root

if __name__ == "__main__":

    filedir = "Data/"
    files = []
    for f in os.listdir(filedir):
        if '.txt' in f:
            files.append(filedir+f)
    files = sorted(files)

    equity = "AAPL"
    balance = 10000.0
    stockcounter = 1
    while 1:
        with open("Data/"+equity+".txt", "r") as f:
            with open("stock", "w") as stockf:
                print >> stockf, equity
                print "STOCK", equity
            for lineno, line in enumerate(f):
                skip = False
                for r in ['=', 'EXCHANGE']:
                    if r in line:
                        skip = True
                if skip:
                    continue
                date, close, high, low, _open, volume = line.strip().split(',')
                with open("price", "w") as pricef:
                    print >> pricef, high
                    print "PRICE", high
                with open("action", "r") as actionf:
                    action = actionf.read().strip()
                    print "ACTION", action
                    high = float(high)
                    if action == "BUY":
                        balance -= high
                        stockcounter += 1
                    if action == "SELL":
                        if stockcounter >= 1:
                            balance += high
                        stockcounter -= 1
                        if stockcounter < 0:
                            stockcounter = 0
                    with open("balance", "w") as balancef:
                        print >> balancef, balance
                        print "BALANCE", balance

                    if "SWITCH" in action:
                        equity = random.choice(files)
                        print equity
                        equity = path_leaf(equity)
                        print equity
                        balance += high * stockcounter
                        stockcounter = 0
                        time.sleep(5)
                        break
                print "EQUITY", equity
                time.sleep(5)
        equity = random.choice(files)
        print equity
        equity = path_leaf(equity)
        print equity
        balance += high * stockcounter
        stockcounter = 0
        time.sleep(5)