import matplotlib.pyplot as plt
import requests
import pandas as pd
import datetime


class GetPhotoTrade:
    """
    -------------------------------------------------------
    This class represents the process of obtaining an image
    that describes the situation of bitcoin in real time
    ------------------------------------------------------
    __data_x - list of time checking trading data
    __data_y - list of values of price
    __url - string value which contains websockets for parsing
    """
    __url = f'https://api.coingecko.com//api//v3/coins/'

    def __init__(self, cryptocurrency, interval):
        plt.style.use('dark_background')
        self.crypto_name = cryptocurrency
        self.market_info = self.get_market_chart(cryptocurrency, 'eur', interval)
        self.set_photo()

    def set_photo(self):
        plt.style.use('dark_background')
        if self.crypto_name == 'bitcoin':
            self.market_info.plot(y='price', x='timestamp', color='#ff8000')
        elif self.crypto_name == 'cardano':
            self.market_info.plot(y='price', x='timestamp', color='#4285f4')
        elif self.crypto_name == 'ethereum':
            self.market_info.plot(y='price', x='timestamp', color='#ffff00')
        elif self.crypto_name == 'solana':
            self.market_info.plot(y='price', x='timestamp', color='#7fffd4')

        plt.savefig('output.png')

    @staticmethod
    def availiable_crypto():
        url = f'https://api.coingecko.com/api/v3/coins'
        response = requests.get(url)
        data = response.json()

        crypto_ids = []

        for asset in data:
            crypto_ids.append(asset['id'])

        return crypto_ids

    def get_market_chart(self, coind_id='bitcoin', vs_currency='eur', days='max', interval='daily'):
        crypto_ids = self.availiable_crypto()
        if coind_id in crypto_ids:
            url = f'https://api.coingecko.com//api//v3/coins/{coind_id}/market_chart'
            payload = {'vs_currency': vs_currency,
                       'days': days,
                       'interval': interval
                       }
            response = requests.get(url, params=payload)
            data = response.json()

            timesmap_list = []
            price_list = []

            for price in data['prices']:
                timesmap_list.append(datetime.datetime.fromtimestamp(price[0] // 1000))
                price_list.append(price[1])

            raw_data = {
                'timestamp': timesmap_list,
                'price': price_list
            }

            df = pd.DataFrame(raw_data)
            return df
        else:
            print('The crypto is not availiable')


    # new = GetPhotoTrade('cardano', '30')
    # new.set_photo()







