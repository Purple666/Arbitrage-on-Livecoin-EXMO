import requests
import time


def getprices():
    response = requests.get('https://api.livecoin.net/exchange/ticker?currencyPair=BTC/USD')
 
    m = response.json()
   
    bestbid1 = m['best_bid']
    bestask1 = m['best_ask']

    response = requests.get('https://poloniex.com/public?command=returnTicker')
    m = response.json()
    
    bestbid2 = float(m['USDT_BTC']['highestBid'])
    bestask2 = float(m['USDT_BTC']['lowestAsk'])

    bid1 = bestbid1
    ask1 = bestask1
    bid2 = bestbid2
    ask2 = bestask2
    return bid1, ask1, bid2, ask2


def check():
    bid1, ask1, bid2, ask2 = getprices()
    
    # arbitrage = 'NO'
    if ((bid1 / ask2) > 1.01):
        arbitrage = 'POLO'
    elif ((bid2 / ask1) > 1.01):
        arbitrage = 'LIVE'
    else:
        arbitrage = 'NO'
        return arbitrage




import telebot

token = '554253191:AAFDkj6jfMdq3LJ0HgkI2wk3CxmgP5OL7-M'

bot = telebot.TeleBot(token)

CHANNEL_NAME = '@moneygunforme'


def SendMessage(arbitrage):
    bid1, ask1, bid2, ask2 = getprices()
    profitL = (bid1 / ask2 - 1) * 100
    profitE = (bid2 / ask1 - 1) * 100

    if (arbitrage == 'NO'):
        bot.send_message(CHANNEL_NAME, 'BTC/USD \nPrepare to close all positions!')
    if (arbitrage == 'LIVE'):
        bot.send_message(CHANNEL_NAME, 'BTC/USD \nBUY on LiveCoin, SELL on Poloniex \n Estimated profit: ' + str(profitL))
    if (arbitrage == 'POLO'):
        bot.send_message(CHANNEL_NAME, 'BTC/USD \nBUY on Poloniex, SELL on LiveCoin \n Estimated profit: ' + str(profitE))
    time.sleep(1)


a2 = 'NO'

iteration = 0;
bot.send_message(CHANNEL_NAME, 'Bot Started!')
while (True):
    time.sleep(10)
    a1 = check()
    if (not a1 == a2):
        SendMessage(a1)

    a2 = a1
    iteration += 1;
    print(iteration)
