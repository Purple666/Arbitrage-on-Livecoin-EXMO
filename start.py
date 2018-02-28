import requests
import time
def getprices():

    response = requests.get('https://api.livecoin.net/exchange/ticker?currencyPair=BTC/USD')
    #print(response.content)
    m=response.content
    #print(type(m))
    #print(len(m))
    S=''
    for i in range(0,len(m),1):
        S=S+chr(m[i])
    #print(S)

    bb1=S.find('best_bid":',0,len(m))
    bb2=S.find(',',bb1,len(m))

    #print(bb1+10)
    bestbid=float(S[bb1+10:bb2:1])
    #print(bestbid)

    ba1=S.find('best_ask":',0,len(m))
    ba2=S.find('}',bb1,len(m))

    #print(ba1+10)
    bestask=float(S[ba1+10:ba2:1])
    #print(bestask)
    #


    response = requests.get('https://api.exmo.com/v1/ticker/')
    ##print(response.content)
    m=response.content
    #print(type(m))


    S=''
    for i in range(0,len(m),1):
        S=S+chr(m[i])
    #print(S)
    btcusd=S.find('BTC_USDT',0,len(m))
    #print(btcusd)
    bp1=S.find('buy_price":"',btcusd,len(m))
    bp2=S.find('",',bp1,len(m))

    #print(S[bb1+11:bb2:1])
    buyprice=float(S[bp1+12:bp2:1])
   # print(buyprice)

    sp1=S.find('sell_price":"',btcusd,len(m))
    sp2=S.find('",',sp1,len(m))

    #print(ba1+10)
    sellprice=float(S[sp1+13:sp2:1])
   # print(sellprice)
    bid1 = bestbid
    ask1 = bestask
    bid2 = buyprice
    ask2 = sellprice
    return bid1,ask1,bid2,ask2

def check():
    bid1,ask1,bid2,ask2=getprices()
    #print(bid1,ask1,bid2,ask2)
    arbitrage='NO'
    if ((bid1/ask2)>1.01):
        arbitrage='EXMO'
    elif ((bid2/ask1)>1.01):
        arbitrage='LIVE'
    else:
        arbitrage = 'NO'
        return arbitrage

import telebot
token='554253191:AAFDkj6jfMdq3LJ0HgkI2wk3CxmgP5OL7-M'

bot = telebot.TeleBot(token)

CHANNEL_NAME = '@moneygunforme'

def SendMessage(arbitrage):
    bid1, ask1, bid2, ask2 = getprices()
    profitL=(bid1/ask2-1)*100
    profitE = (bid2 / ask1-1)*100

    if (arbitrage=='NO'):
        bot.send_message(CHANNEL_NAME, 'BTC/USD \nPrepare to close all positions!')
    if (arbitrage=='LIVE'):
        bot.send_message(CHANNEL_NAME, 'BTC/USD \nBUY on LiveCoin, SELL on EXMO \n Estimated profit: '+str(profitL))
    if (arbitrage=='EXMO'):
        bot.send_message(CHANNEL_NAME, 'BTC/USD \nBUY on EXMO, SELL on LiveCoin \n Estimated profit: '+str(profitE))
    time.sleep(1)


a2='NO'

iteration = 0;
bot.send_message(CHANNEL_NAME, 'Bot Started!')
while (True):
    time.sleep(10)
    a1=check()
    if (not a1==a2):
        SendMessage(a1)
    a2=a1
    iteration+=1;
    print(iteration)
