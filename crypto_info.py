import cryptocompare as crypto


class CryptoInfo:
    """
    This class represents information about the cryptocurrency
    on the market at a given time
    """
    __list_crypto = ['ETH', 'BTC', 'BNB', 'USDT', 'SOL']

    def __init__(self, crypto_name):
        if not isinstance(crypto_name, str):
            raise TypeError('The type of crypto_index must be string')
        if crypto_name not in CryptoInfo.__list_crypto:
            raise ValueError('The value of crypto_name must be in the list of crypto_info')
        self.type_crypto = crypto_name
        self.__price_crypto = crypto.get_price(self.type_crypto)[self.type_crypto]['EUR']

    @property
    def price_crypto(self):
        return self.__price_crypto
