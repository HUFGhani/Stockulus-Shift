#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, Response, g
from super_shift import StockulusShift

app = Flask(__name__)

def get_game():
    game = getattr(g, '_game', None)
    if game == None:
        game = g._game = StockulusShift()
    return game

@app.teardown_appcontext
def close_connection(exception):
    game = getattr(g, '_game', None)
    if game is not None:
        game.release()

@app.route("/get_price")
def get_price():
    game = get_game()
    print game.crt_price
    return str(game.crt_price)

@app.route("/get_shares")
def get_crt_stock():
    game = get_game()
    return str(game.shares)

@app.route("/get_stock")
def get_stock():
    game = get_game()
    return str(game.stock)

@app.route("/get_balance")
def get_balance():
    game = get_game()
    return str(game.balance)

@app.route("/get_move")
def get_move():
    game = get_game()
    return str(game.crt_move)

@app.route("/")
def get_everything():
    game = get_game()
    stock = game.stock
    shares = game.shares
    price = game.crt_price
    resp = "%s,%s,%s" % (stock, shares, price)
    return resp

@app.route("/update")
def update():
    game = get_game()
    game.update() 

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.debug = True
    app.run()
