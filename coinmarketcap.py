
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import asyncio
from math import log10 , floor

default_coins = ['BTC','ETH','DOGE']

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  #'symbol': symbols,
  'skip_invalid': True
}

# get your own API key from coinmarketcap
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'XXXXXXXXXXXXXXXXXXXXXXXXXX',
}

def round_it(x, sig):
    return round(x, sig-int(floor(log10(abs(x))))-1)

#print(round_it(1.3524,4))

async def getquotes(symblist = False):
    session = Session()
    session.headers.update(headers)

    symbols_list = default_coins[:]

    if symblist:
        for s in symblist:
            symbols_list.insert(0, str(s).upper())

    symbols = ','.join(symbols_list)
    print(symbols)
    parameters['symbol'] = symbols

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        #print(data)
        output = ""
        for token in symbols_list:
            try:
                value = data['data'][token]
                quote = data['data'][token]['quote']['USD']
                if quote['price'] > 10000:
                    price = round(quote['price'])
                else:
                    price = round_it(quote['price'], 5)
            except:
                continue

            if quote['price'] < 0.01:
                format_str = "**{}**: {:.3e} {:.1f}%"
            else:
                format_str = "**{}**: {} {:.1f}%"

            output = output + format_str.format(value['symbol'], price, quote['percent_change_24h']) + "\n"

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return output



