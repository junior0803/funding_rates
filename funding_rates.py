import ccxt
import csv
import pandas as pd
from datetime import datetime
import time

print('CCXT Version:', ccxt.__version__)
from pprint import pprint


exchange = ccxt.binance({
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future',
    },
})

#pprint(response)
def get_response(startTime, endTime):
    pprint("startTime = " + str(startTime) + " endTime = "  + str(endTime))

    markets = exchange.load_markets()
    # exchange.verbose = True  # uncomment for debugging
    symbol = 'ETH/USDT'
    market = exchange.market(symbol)

    response = exchange.fapiPublic_get_fundingrate({
        'symbol': market['id'],
        'startTime': startTime,  # ms to get funding rate from INCLUSIVE.
        'endTime': endTime,  # ms to get funding rate until INCLUSIVE.
        'limit':1000, # limit
    })
    df = pd.DataFrame(response)
    return df

def main():
    startTime = exchange.parse8601('2018-11-25T00:00:00Z')
    endTime = exchange.parse8601(datetime.today().isoformat())
    lastDf = get_response(startTime, endTime)
    CurTime = lastTime = lastDf['fundingTime'].iloc[-1]
    lastDf.to_csv('filename.csv', 'w', header=True, index=True)
    while True:
        time.sleep(5)
        CurDf = get_response(CurTime, endTime)
        CurTime = CurDf['fundingTime'].iloc[-1]
        if (CurTime == lastTime) : 
            pprint('break')
            break
        else:
            CurDf.to_csv('filename.csv', 'a', header=True, index=True)
            lastTime = CurTime

main()

