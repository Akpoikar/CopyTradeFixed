import TgBot
import bybit
from Person import Position

import os
import ta
import ccxt
import time
import json
import uuid
import random
import sqlite3
import datetime
import pandas as pd
from inspect import currentframe
import pybit
from binance.client import Client
from colorama import init, Fore, Back, Style
from pybit.unified_trading import HTTP
file1 = open('config.txt', 'r')
lines = file1.read().splitlines()
API_Key = lines[0]
Secret_Key = lines[1]
file1.close()

# exchange = ccxt.bybit({'apiKey':API_Key,'secret':Secret_Key})
client = HTTP(testnet=False,api_key=API_Key,api_secret=Secret_Key)
client1 = bybit.bybit(test=False,api_key=API_Key,api_secret=Secret_Key)
# exchange.create_market_order("BTCUSDT","sell",'0.002')

info = client1.Market.Market_symbolInfo().result()
symbols = client1.Symbol.Symbol_get().result()
syms = symbols[0]['result']

# bal =client.get_wallet_balance(accountType ='UNIFIED')


def GetPrice(symbol):
    client1 = bybit.bybit(test=False,api_key=API_Key,api_secret=Secret_Key)
    info = client1.Market.Market_symbolInfo().result()
    keys = info[0]['result']
    for k in keys:
        if k['symbol'] == symbol:
            price = k['last_price']
            return price


def GetSymbolStep(symbol):
    for s in syms:
        if s['name'] == symbol:
            return s['lot_size_filter']['qty_step']

def ChangeLeverage(positionToIns, lever):
    try:
        client.set_leverage(category="linear", symbol=positionToIns.symbol, buyLeverage=lever, sellLeverage=lever)
    except Exception as e:
        a = 5

def CreateOrder(positionToIns,side):
    client = HTTP(testnet=False,api_key=API_Key,api_secret=Secret_Key)

    ratio = TgBot.GetRatio()

    laverage = int(TgBot.GetLeverage())
    if laverage == 0:
        laverage = int(positionToIns.leverage)

    client.set_leverage(category="linear", symbol=positionToIns.symbol, buyLeverage=str(laverage), sellLeverage=str(laverage))


    price = GetPrice(positionToIns.symbol)
    q = GetSymbolStep(positionToIns.symbol)

    amount = ratio/float(price)
    qt = amount * laverage

    num1 = float(qt)/float(q)
    inter = int(num1)
    num2 = inter * float(q)

    Term = ''
    if side == True:
        Term = 'Buy'
    else:
        Term = 'Sell' 

    client.place_order(
        category="linear",
        symbol=positionToIns.symbol,
        side=Term,
        orderType="Market",
        qty=num2,
        timeInForce="GoodTillCancel",
    )

def UpdateOrder(positionToIns,side,amount):
    client = Client(API_Key, Secret_Key)
    ratio = TgBot.GetRatio()
    laverage = TgBot.GetLeverage()
    sym = client.futures_symbol_ticker(symbol = positionToIns.symbol)
    # laverage = maxLeverage(symbol1)
    if laverage == 0:
        laverage = int(positionToIns.leverage)
    client.futures_change_leverage(symbol=positionToIns.symbol,leverage=laverage)

    precision = GetPrecision(positionToIns.symbol)
    q = abs(ratio * amount)
    q = float("{:.{}f}".format(q,precision))
    Term = ''
    if side == True:
        Term = 'BUY'
    else:
        Term = 'SELL' 
    
    if Term == "SELL" and amount > 0:
        Term = 'BUY'
    if Term == 'BUY' and amount < 0:
        Term = 'SELL'
    client.futures_create_order(
        symbol=positionToIns.symbol,
        type='MARKET',
        side=Term,
        quantity=q
    )

def CloseAllOrders():
    orders = client.futures_account()['positions']

    for o in orders:
        if float(o['maintMargin']) > 0:
            CloseOrder(o['symbol'])


def CloseOrder(Pos):
    client = HTTP(testnet=False,api_key=API_Key,api_secret=Secret_Key)

    pos = client.get_positions(category="linear",openOnly=1,
    limit=1,symbol=Pos,)

    res = pos['result']['list'][0]
    qt = res['size']
    if qt == '0':
        return
    price = res['markPrice']
    Term = res['side']
    if Term == 'Buy':
        Term = 'Sell'
    elif Term == 'Sell':
        Term = 'Buy'
    client.place_order(
        category="linear",
        symbol=Pos,
        side=Term,
        orderType="Market",
        qty=qt,
        price=price,
        timeInForce="GoodTillCancel",
        reduceOnly=True
    )

# CloseAllOrders()
# CloseOrder('BTCUSDT')
#info = client.get_symbol_info(symbol='BNBBTC')
print('End')