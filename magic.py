import datetime as dt
import matplotlib.pyplot as plt
import pandas_datareader as web


def get_photo():
    plt.style.use('dark_background')

    ma_1 = 30
    ma_2 = 100

    start = dt.datetime.now() - dt.timedelta(days=50)
    end = dt.datetime.now()

    data = web.DataReader('BTC', 'yahoo', start, end)
    data['SMA_5'] = data['Adj Close'].rolling(5).mean()
    data['SMA_20'] = data['Adj Close'].rolling(20).mean()

    data = data.iloc[20:]

    buy_signals = []
    sell_signals = []

    trigger = 0
    debil_buy = dt.datetime.now()
    debil_sell = dt.datetime.now()

    for x in (range(len(data))):
        if data['SMA_5'].iloc[x] > data['SMA_20'].iloc[x] and trigger != 1:
            buy_signals.append(data['Adj Close'].iloc[x])
            sell_signals.append(float('nan'))
            debil_buy = data['Adj Close'].iloc[x]
            trigger = 1

        elif data['SMA_5'].iloc[x] < data['SMA_20'].iloc[x] and trigger != -1:
            buy_signals.append(float('nan'))
            sell_signals.append(data['Adj Close'].iloc[x])
            trigger = -1
            debil_sell = data['Adj Close'].iloc[x]

        else:
            buy_signals.append(float('nan'))
            sell_signals.append(float('nan'))

    data['Buy Signals'] = buy_signals
    data['Sell Signals'] = sell_signals

    plt.plot(data['Adj Close'], label='Share Price', alpha=0.5)
    plt.plot(data['SMA_5'], label='SMA_5', color='orange', linestyle="--")
    plt.plot(data['SMA_20'], label='SMA_20', color='pink', linestyle="--")
    plt.scatter(data.index, data['Buy Signals'], label="Buy Signal", marker="^", color="#00ff00", lw=3)
    plt.scatter(data.index, data['Sell Signals'], label="Sell Signal", marker="v", color="#ff0000", lw=3)

    plt.legend(loc="upper left")
    plt.savefig('output.png')
    return 'output.png'


