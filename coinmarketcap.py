
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import asyncio
from math import log10 , floor

default_coins = ['BTC','ETH','DOGE']
default_coins = [1, 1027, 74]

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
  #'symbol': symbols,
  'skip_invalid': True
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
}

def round_it(x, sig):
    return round(x, sig-int(floor(log10(abs(x))))-1)

#print(round_it(1.3524,4))

id_map = dict()

def get_id_map(s):
    global id_map

    if len(id_map) == 0:
        print("getting list of all tokens and coins")
        session = Session()
        session.headers.update(headers)

        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/map"
        parameters = {
            # 'symbol': symbols,
            'sort': "cmc_rank"
        }

        try:
            response = session.get(url, params=parameters)
            data = json.loads(response.text)
            for i in data['data']:
                symb = i['symbol'].upper()
                if not (symb in id_map):
                    id_map[symb] = []
                id_map[symb].append(i['id'])

        except (ConnectionError, Timeout, TooManyRedirects) as e:
            print(e)

    return id_map[s.upper()]


#print(get_id_map('doge'))

async def getquotes(symblist = False):
    session = Session()
    session.headers.update(headers)

    id_list = []
    if symblist:
        for s in symblist:
            id_list = id_list + get_id_map(s)

    id_list = id_list + default_coins
    id_list = list(map(str, id_list))
    print(id_list)

    id_list_str = ','.join(id_list)
    print(id_list_str)
    parameters['id'] = id_list_str

    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        #print(data)
        output = ""
        for token in id_list:
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
                format_str = "**{}** {}: {:.3e} {:.1f}%"
            else:
                format_str = "**{}** {}: {} {:.1f}%"

            output = output + format_str.format(value['symbol'], value['slug'], price, quote['percent_change_24h']) + "\n"

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)

    return output


#print( getquotes(["avax"]))
