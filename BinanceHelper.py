import TgBot
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
from Person import Position
file1 = open('config.txt', 'r')
lines = file1.read().splitlines()
API_Key = lines[0]
Secret_Key = lines[1]
file1.close()



client = Client(API_Key, Secret_Key)
print('Logged In')

# depth = client.futures_historical_klines(
#     symbol='BTCUSDT',
#     interval='1d',  # can play with this e.g. '1h', '4h', '1w', etc.
#     start_str='2022-11-03',
#     end_str='2022-11-04'
# )

btc_price = client.get_symbol_ticker(symbol="DOGEUSDT")
info = client.get_account()
# client.futures_change_leverage(symbol='DOGEUSDT',leverage=1)
for i in info["balances"]:
    if float(i['free']) > 0:
        print(i)

acc_balance = client.futures_account_balance()

for check_balance in acc_balance:
    if check_balance["asset"] == "USDT":
        usdt_balance = check_balance["balance"]
        print(usdt_balance)
def maxLeverage(pair):
    result = client.futures_leverage_bracket()
    res = client.futures_coin_leverage_bracket()
    for x in result:
        if x['symbol'] == pair:
            hallow = x['brackets'][-5]
    return(hallow['initialLeverage'])


exchangeinfo = client.futures_exchange_info()
def GetPrecision(symbol):
    requestedFutures = []
    requestedFutures.append(symbol)
    val={si['symbol']:si['quantityPrecision'] for si in exchangeinfo['symbols'] if si['symbol'] in requestedFutures}
    return val[symbol]

def ChangeLeverage(positionToIns):
    client.futures_change_leverage(symbol=positionToIns.symbol,leverage=positionToIns.leverage)

def CreateOrder(positionToIns,side):
    client = Client(API_Key, Secret_Key)
    ratio = TgBot.GetRatio()
    sym = client.futures_symbol_ticker(symbol = positionToIns.symbol)
    laverage = TgBot.GetLeverage()
    if laverage == 0:
        laverage = int(positionToIns.leverage)

    client.futures_change_leverage(symbol=positionToIns.symbol,leverage=laverage)

    num = (ratio)/float(sym['price'])
    q=float(laverage*num)
    precision = GetPrecision(positionToIns.symbol)
    # q = abs(ratio * positionToIns.amount)  
    #q = ratio
    q = float("{:.{}f}".format(q,precision))
    Term = ''
    if side == True:
        Term = 'BUY'
    else:
        Term = 'SELL' 
    client.futures_create_order(
        symbol=positionToIns.symbol,
        type='MARKET',
        side=Term,
        quantity=q
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


orders = client.futures_account()['positions']
a = 0
for o in orders:
        if float(o['maintMargin']) > 0:
         a+=float(o['unrealizedProfit'])
         print (o['symbol'] + ' ' + o['maintMargin'] +' '+o['leverage']+' '+ o['unrealizedProfit'])
print(a)

def CloseAllOrders():
    orders = client.futures_account()['positions']

    for o in orders:
        if float(o['maintMargin']) > 0:
            CloseOrder(o['symbol'], 'SELL')
            continue
            precision = GetPrecision(o['symbol'])
            q = float("{:.{}f}".format((-1*float(o['positionAmt'])),precision))    
            client.futures_create_order(
                symbol=o['symbol'],
                type='MARKET',
                side='SELL',
                quantity=str(abs(q))
            )

# CloseAllOrders()

def CloseOrder(Pos, side):
    client = Client(API_Key, Secret_Key)
    orders = client.futures_account()['positions']
    
    for o in orders:
        if float(o['maintMargin']) > 0 and o['symbol'] == Pos:
         
            Term = ''
            if side == True:
                Term = 'BUY'
            else:
                Term = 'SELL'

            precision = GetPrecision(Pos)
            q = float("{:.{}f}".format((float(o['positionAmt'])),precision))
            client.futures_create_order(
                symbol=o['symbol'],
                type='MARKET',
                side=Term,
                quantity=str(abs(q))
            )

# CloseAllOrders()
# CloseOrder('RVNUSDT',False)
#info = client.get_symbol_info(symbol='BNBBTC')
print('End')