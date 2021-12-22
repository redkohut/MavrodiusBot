import websockets
import asyncio
import time
import matplotlib.pyplot as plt
import config
import logging
from aiogram import Bot, Dispatcher, executor, types
from sqlController import SQLighter
import magic
from datetime import datetime

# set level logging
logging.basicConfig(level=logging.INFO)

# Initialize bot with database(sqlite)
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
db = SQLighter('clientdb.db')

fig = plt.figure()
ax = fig.add_subplot(111)
fig.show()

xdata = []
ydata = []


def update_graph():
    ax.plot(xdata, ydata, color='g')
    ax.legend([f"Last price: {ydata[-1]}$"])

    fig.canvas.draw()
    plt.savefig('dateNow.png')
    plt.pause(0.1)


count_decrease = []
count_uncrease = []


async def main(wait_for):
    url = "wss://stream.binance.com:9443/stream?streams=btcusdt@miniTicker"
    async with websockets.connect(url) as client:
        # data = json.loads(await client.recv())['data']
        data = client.recv()['data']

        start_sum = float(data['c'])
        time_now = int(time.time())
        count = 0
        while True:
            data = client.recv()['data']

            event_time = time.localtime(data['E'] // 1000)
            event_time = f"{event_time.tm_hour}:{event_time.tm_min}:{event_time.tm_sec}"

            xdata.append(event_time)
            ydata.append(int(float(data['c'])))
            # check time
            a = int(time.time() - time_now)
            if a % 1 == 0:
                print(count)
                count += 1

            current_sum = float(data['c'])
            if current_sum >= start_sum and count < 10:
                start_sum = float(data['c'])
                count = 0

                subscriptions = db.get_subscriptions()

                for user in subscriptions:
                    await bot.send_photo(
                        user[1],
                        photo=open(magic.get_photo(), 'rb'),
                        caption="Buy!!! Increase bitcoin",
                        disable_notification=True)
            elif current_sum < start_sum and count < 10:
                start_sum = float(data['c'])
                count = 0

                subscriptions = db.get_subscriptions()
                for user in subscriptions:
                    await bot.send_photo(
                        user[1],
                        photo=open(magic.get_photo(), 'rb'),
                        caption="Sell!!! Decrease bitcoin",
                        disable_notification=True)
            elif count >= 10:
                cout = 0
                start_sum = float(data['c'])


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        # if the user is not in the database, add it
        db.add_subscriber(message.from_user.id)
    else:
        # if it already have, we just update his status 'following'
        db.update_subscription(message.from_user.id, True)

    await message.answer(
        "Вы успешно подписались на рассылку!\nЖдите, скоро выйдут новые обзоры и вы узнаете о них первыми =)")


# Команда отписки
@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if (not db.subscriber_exists(message.from_user.id)):
        # if the user is not in the database, add negative status
        db.add_subscriber(message.from_user.id, False)
        await message.answer("Вы итак не подписаны.")
    else:
        # if it already have, we just update his negative status
        db.update_subscription(message.from_user.id, False)
        await message.answer("Вы успешно отписаны от рассылки.")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main(10))
    executor.start_polling(dp, skip_updates=True)

