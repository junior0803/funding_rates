# -*- coding: utf-8 -*-


import os
import sys
import pandas as pd
import time

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

import ccxt  # noqa: E402

print('CCXT Version:', ccxt.__version__)

def table(values):
    first = values[0]
    keys = list(first.keys()) if isinstance(first, dict) else range(0, len(first))
    widths = [max([len(str(v[k])) for v in values]) for k in keys]
    string = ' | '.join(['{:<' + str(w) + '}' for w in widths])
    return "\n".join([string.format(*[str(v[k]) for k in keys]) for v in values])


exchange = ccxt.ftx({
    'headers': {
        'FTX-SUBACCOUNT': 'x_SR_ETH',
    },
    'enableRateLimit': True,
    'apiKey': 'rgGwnE3ZikQqPCfecXCQ1D0gzsm5WyoEHdDvFCUi', # YOUR_API_KEY
    'secret': '5G214mjkAjuhDbZK1kiVrAVjgOa7Gxl_UXhZKmd1', # YOUR_SECRET
})

start = exchange.parse8601('2020-01-01T00:00:00Z')  # timestamp in milliseconds
end = exchange.parse8601('2020-05-02T00:00:00Z')  # current timestamp in milliseconds
#end = exchange.milliseconds()  # current timestamp in milliseconds
allresult = []
while True:
    time.sleep(1)

    request = {
        'start_time': int(start / 1000),  # unix timestamp in seconds, optional
        'end_time': int(end / 1000),  # unix timestamp in seconds, optional
        # 'future': 'BTC-PERP',  # optional
    }

    response = exchange.public_get_funding_rates(request)
    result = exchange.safe_value(response, 'result', [])
    tempTime = exchange.parse8601(result[-1]['time'])
    if (start == tempTime):
        break
    end = tempTime
    print(table(result))
    allresult += result


df = pd.DataFrame(allresult)
df.to_csv('funding_rates.csv', index=False)