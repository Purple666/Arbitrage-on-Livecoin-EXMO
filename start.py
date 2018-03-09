import requests
import time

isvaluable=['NO','NO','NO','NO']
pairL=['','BTC/USD','ETH/USD','LTC/USD']
pairP=['','USDT_BTC','USDT_ETH','USDT_LTC']
pairvalue=[0,0,0,0]
def getprices(npair):
    response = requests.get('https://api.livecoin.net/exchange/ticker?currencyPair='+pairL[npair])
    m = response.json()

    bestbid1 = m['best_bid']
    bestask1 = m['best_ask']

    response = requests.get('https://poloniex.com/public?command=returnTicker')
    m = response.json()

    bestbid2 = float(m[pairP[npair]]['highestBid'])
    bestask2 = float(m[pairP[npair]]['lowestAsk'])

    bid1 = bestbid1
    ask1 = bestask1
    bid2 = bestbid2
    ask2 = bestask2
    return bid1, ask1, bid2, ask2


def check(npair):
    bid1, ask1, bid2, ask2 = getprices(npair)
    value=0
    value1 = bid1 / ask2
    value2 = bid2 / ask1
    arbitrage = False
    if value1>1.015:
        value=value1
        arbitrage='LIVE'
    if value2 > 1.015:
        value = value2
        arbitrage = 'POLO'

    return arbitrage, value




import telebot
token = '554253191:AAFDkj6jfMdq3LJ0HgkI2wk3CxmgP5OL7-M'
bot = telebot.TeleBot(token)
CHANNEL_NAME = '@moneygunforme'

isvaluable0=['NO','NO','NO','NO']
def SendMessage():
    for np in range(1, 3 + 1, 1):
        isvaluable0[np]=isvaluable[np]
    print(isvaluable0, isvaluable)

    for np in range(1,3+1,1):
        arbitrage,value=check(np)
        pairvalue[np]=value
        isvaluable[np]=arbitrage
        print(isvaluable0, isvaluable)

    if (not (isvaluable0==isvaluable)):
        S=''
        S='Valuable pairs is available:'
        for np in range(1, 3 + 1, 1):
            if ( not (isvaluable[np]=='NO')):
                S+='\n'+pairL[np]+' - profit: '+str(round(pairvalue[np],5))+', buy on '+isvaluable[np]

        bot.send_message(CHANNEL_NAME, S)
    else:
        print('no changes',isvaluable0,isvaluable,pairvalue)
    time.sleep(1)

bot.send_message(CHANNEL_NAME, 'Bot Started')
while True:
    #try:
    SendMessage()
    #except BaseException:
    #    print('Error, check log')
