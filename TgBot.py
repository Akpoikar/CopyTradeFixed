from concurrent.futures import thread
import telebot
import threading
import time
import datetime
from Person import BettingPosition

file1 = open('config.txt', 'r')
lines = file1.read().splitlines()
API_Key = lines[2]
chat_id = int(lines[3])
ratio = float(lines[4])
name = lines[5]
file1.close()

bot = telebot.TeleBot(API_Key)

UsersToFollow = []
BettingPositions = []

@bot.message_handler(commands=['follow'])
def Follow(msg):
    try:
        messageText = msg.text.split()[1]
        if  messageText not in UsersToFollow:
            UsersToFollow.append(messageText)
            bot.reply_to(msg,'You are following ' + messageText)
    except:
        print ('Error')

@bot.message_handler(commands=['showall'])
def Greetings(msg):
    try:
        for item in UsersToFollow:
            bot.send_message( chat_id,item )
    except:
        print ('Error')

@bot.message_handler(commands=['setratio'])
def SetRatio(msg):
    try:
        global ratio
        messageText = msg.text.split()[1]
        ratio = float(messageText)
    except:
        print ('Error')


@bot.message_handler(commands=['unfollow'])
def UnFollow(msg):
    try:
        messageText = msg.text.split()[1]
        if messageText in UsersToFollow:
            UsersToFollow.remove(messageText)
            bot.reply_to(msg,'You are not following ' + messageText)

    except:
        print ('Error')


@bot.message_handler(commands=['start'])
def Greetings(msg):
    chat_id = msg.chat.id 
    bot.send_message( chat_id,'Welcome')

def SendAllUsers(tmpUser, positionToIns):
    try:
        if tmpUser.id in UsersToFollow:
                epoch = datetime.datetime.fromtimestamp(positionToIns.time/1000.0)           
                date = str(epoch.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])

                msgId = bot.send_message( chat_id,name + '\n' +"🚨Open : " + tmpUser.name +'\nTime: ' + date + '\n\n' +"Symbol: " + positionToIns.symbol + '\n' + '\nAmount:' + str(positionToIns.amount) + '\n' + 'Type: ' + positionToIns.term + '\n' + 'Market price: ' + str(positionToIns.entryPrice) + '\nLeverage : ' + str(positionToIns.leverage))
                pos = BettingPosition(tmpUser.id,positionToIns.symbol,msgId)
                BettingPositions.append(pos)
    except Exception as e:
        print ("Failed : {0}\n".format(str(e)))

def SendAllUsers1(tmpUser, positionToIns):
    try:
        if tmpUser.id in UsersToFollow:
            epoch = datetime.datetime.fromtimestamp(positionToIns.time/1000.0)           
            date = str(epoch.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
            pnl = ''
            roe = ''
            if positionToIns.pnl > 0:

                pnl = str("{:.2f}".format(positionToIns.pnl))
                roe = '+' + str("{:.2f}".format(positionToIns.roe)) +  '% ✅'
            else:
                pnl = str("{:.2f}".format(positionToIns.pnl))
                roe = str("{:.2f}".format(positionToIns.roe)) + '% ❌'
            for bet in BettingPositions:
                if(bet.userId == tmpUser.id and positionToIns.symbol == bet.symbol):
                    bot.reply_to( bet.msgid,name + '\n' +"🔒Close: " + tmpUser.name +'\nTime: ' + date + '\n\n' +"Symbol : " + positionToIns.symbol + '\n' +"Amount : " + str(positionToIns.amount) + '\n' + 'Type: ' + positionToIns.term + '\n' + 'Open price: ' + str(positionToIns.entryPrice) + '\nClosing price: ' + str(positionToIns.markPrice) + '\nPnL: ' + pnl + '\nRoe: ' + roe+ '\nLeverage : ' + str(positionToIns.leverage))
                    BettingPositions.remove(bet)
                    break
    except Exception as e:
        print ("Failed : {0}\n".format(str(e)))

def SendAllUsersChange(tmpUser, positionToIns, text):
    try:
        if tmpUser.id in UsersToFollow:
            epoch = datetime.datetime.fromtimestamp(positionToIns.time/1000.0)           
            date = str(epoch.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
            pnl = ''
            roe = ''
            if positionToIns.pnl > 0:
                pnl = str("{:.2f}".format(positionToIns.pnl))
                roe = '+' + str("{:.2f}".format(positionToIns.roe)) +  '% ✅'
            else:
                pnl = str("{:.2f}".format(positionToIns.pnl))
                roe = str("{:.2f}".format(positionToIns.roe)) + '% ❌'
            for bet in BettingPositions:
                if(bet.userId == tmpUser.id and positionToIns.symbol == bet.symbol):
                    bot.reply_to( bet.msgid,name + '\n' +"Change " +text+": " + tmpUser.name +'\nTime: ' + date + '\n\n' +"Symbol : " + positionToIns.symbol + '\n' +"Amount : " + str(positionToIns.amount) + '\n' + 'Type: ' + positionToIns.term + '\n' + 'Open price: ' + str(positionToIns.entryPrice) + '\Mark price: ' + str(positionToIns.markPrice) + '\nPnL: ' + pnl + '\nRoe: ' + roe+ '\nLeverage : ' + str(positionToIns.leverage))
                    break
    except Exception as e:
        print ("Failed : {0}\n".format(str(e)))


def SendAllUsersToBet(symbol, term):
    print('SendBet ' + symbol)
    resString = 'Bet on ' + symbol + ' ' + term + '\nUsers who bet: ' + str(len(users)) +'\n'
    
    # for user in users:
    #     resString += user.name +'\n'

    try:
        bot.send_message( chat_id,resString)
    except:
        print ('Error')

def SendAllUsersToClose(symbol, term, additionalText = ""):
    terming = ''
    if term == True:
        terming = 'LONG'
    else:
        terming = 'SHORT'
    resString = 'Close bet on ' + symbol + ' ' + terming + '\n' + additionalText

    try:
        bot.send_message( chat_id,resString)
    except:
        print ('Error')
    
def SendError(text):
        try:
            text =name + '\n' +"AN ERROR OCCURED\n" + text
            bot.send_message( chat_id,text)
        except:
            print ('Error')

def Polling():
    bot.infinity_polling()


def GetAllUsers():
    return UsersToFollow

def GetRatio():
    return ratio 
