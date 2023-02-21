class User:
    Positions = []
    def __init__(self,name,id,pos):
        self.name = name
        self.id = id
        self.Positions = pos

    def __eq__(self, another):
        if another == None:
            return False
        return self.id == another.id
    
    def AddPositions(self, pos):
        self.Positions.extend(pos)

class Position:
    def __init__(self, symbol, entryPrice, markPrice, pnl, roe, time, term,leverage,amount):
        self.symbol = symbol
        self.entryPrice = str(entryPrice)
        self.markPrice = str(markPrice)
        self.pnl = pnl
        self.roe = roe

        self.time = time
        self.term = term
        self.leverage = leverage
        self.amount = amount
    
    def __eq__(self, another):
        if another == None:
         return False
        return self.symbol == another.symbol 
    

class Bet:
    def __init__(self, symbol, side) -> None:
        self.symbol = symbol
        self.side = side
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, str):
            return self.symbol == __o
        return self.symbol == __o.symbol


class BettingPosition:
    def __init__(self, userId, symbol, msgid):
        self.userId = userId
        self.symbol = symbol
        self.msgid = msgid 