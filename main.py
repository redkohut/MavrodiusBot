import websockets
import asyncio
import time
import config
import logging
from aiogram import Bot, Dispatcher, executor, types
from sqlController import SQLighter
from magic import GetPhotoTrade
import json
import buttons_controller as nav
from crypto_info import CryptoInfo as crypto


# set level logging
logging.basicConfig(level=logging.INFO)

# Initialize bot with database(sqlite)
bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot)
db = SQLighter('database.db')

xdata = []
ydata = []

crypto_name = 'bitcoin'
is_check = False


async def checking_info(wait_for):
    url = "wss://stream.binance.com:9443/stream?streams=btcusdt@miniTicker"
    async with websockets.connect(url) as client:
        data = json.loads(await client.recv())['data']
        start_sum = float(data['c'])
        while True:
            await asyncio.sleep(wait_for)
            data = json.loads(await client.recv())['data']
            event_time = time.localtime(data['E'] // 1000)
            event_time = f"{event_time.tm_hour}:{event_time.tm_min}:{event_time.tm_sec}"

            xdata.append(event_time)
            ydata.append(int(float(data['c'])))

            current_sum = float(data['c'])

            if current_sum >= start_sum + 1:
                start_sum = float(data['c'])
                await send_signal('Buy')
            elif current_sum < start_sum - 1:
                start_sum = float(data['c'])
                await send_signal('Sell')


async def send_signal(type_sign):
    new = GetPhotoTrade('bitcoin', '2')
    new.set_photo()
    subscriptions = db.get_subscriptions()
    for user in subscriptions:
        await bot.send_photo(
            user[1],
            photo=open('output.png', 'rb'),
            caption=f'{type_sign}!!! {type_sign} bitcoin',
            disable_notification=True)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Hi, {0.first_name}!'.format(message.from_user),
                           reply_markup=nav.main_menu)


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # if the user is not in the database, add it
        db.add_subscriber(message.from_user.id)
    else:
        # if it already has, we just update his status 'following'
        db.update_subscription(message.from_user.id, True)

    await message.answer(
        'You have successfully subscribed to the mailing list!\n '
        'Wait, new reviews will come out soon and you will be the first to know about them =)')


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    if not db.subscriber_exists(message.from_user.id):
        # if the user is not in the database, add negative status
        db.add_subscriber(message.from_user.id, False)
        await message.answer('You are not subscribed anyway.')
    else:
        # if it already have, we just update his negative status
        db.update_subscription(message.from_user.id, False)
        await message.answer('You have successfully unsubscribed from the mailing list.')


@dp.message_handler()
async def bot_message(message: types.Message):
    global crypto_name, is_check
    if message.text == '🤑 Cryptocurrency price':
        await bot.send_message(message.from_user.id, 'Cryptocurrency menu', reply_markup=nav.scene_crypto)
    elif message.text == '📈 Analyze the market':
        await bot.send_message(message.from_user.id, 'Analyze the market', reply_markup=nav.scene_analyze)
    elif message.text == '👀 Menu':
        await bot.send_message(message.from_user.id, '✔', reply_markup=nav.main_menu)
    elif message.text == '₿ Bitcoin price':
        await bot.send_message(message.from_user.id, 'Bitcoin last price: ' + str(crypto('BTC').price_crypto) + '💶')
    elif message.text == '🌈 Ethereum price':
        await bot.send_message(message.from_user.id, 'Ethereum last price: ' + str(crypto('ETH').price_crypto) + '💶')
    elif message.text == '🦄 Binance coin':
        await bot.send_message(message.from_user.id, 'Binance coin  price: ' + str(crypto('BNB').price_crypto) + '💶')
    elif message.text == '💩 Tether price':
        await bot.send_message(message.from_user.id, 'Tether coin  price: ' + str(crypto('USDT').price_crypto) + '💶')
    elif message.text == '⚡ Solana price':
        await bot.send_message(message.from_user.id, 'Solana coin  price: ' + str(crypto('SOL').price_crypto) + ' 💶')
    elif message.text == '₿ Bitcoin chart':
        crypto_name = 'bitcoin'
        await bot.send_message(message.from_user.id, 'Choice time interval', reply_markup=nav.scene_time)
    elif message.text == '🌈 Ethereum chart':
        crypto_name = 'ethereum'
        await bot.send_message(message.from_user.id, 'Choice time interval', reply_markup=nav.scene_time)
    elif message.text == '🦄 Cardano chart':
        crypto_name = 'cardano'
        await bot.send_message(message.from_user.id, 'Choice time interval', reply_markup=nav.scene_time)
    elif message.text == '⚡ Solana chart':
        crypto_name = 'solana'
        await bot.send_message(message.from_user.id, 'Choice time interval', reply_markup=nav.scene_time)
    elif message.text == '5 hours':
        print('Crypto name: ', crypto_name)
        photo_id = open('output.png', 'rb')
        new = GetPhotoTrade(crypto_name, '5')
        new.set_photo()
        await bot.send_photo(
            message.from_user.id,
            photo_id,
            caption='You can analyze using the informative menu',
            disable_notification=True)
    elif message.text == '10 hours':
        new = GetPhotoTrade(crypto_name, '10')
        new.set_photo()

        await bot.send_photo(
            message.from_user.id,
            photo=open('output.png', 'rb'),
            caption='You can analyze using the informative menu',
            disable_notification=True)
    elif message.text == '15 hours':
        new = GetPhotoTrade(crypto_name, '15')
        new.set_photo()
        await bot.send_photo(
            message.from_user.id,
            photo=open('output.png', 'rb'),
            caption='You can analyze using the informative menu',
            disable_notification=True)
    elif message.text == '30 hours':
        new = GetPhotoTrade(crypto_name, '30')
        new.set_photo()
        await bot.send_photo(
            message.from_user.id,
            photo=open('output.png', 'rb'),
            caption='You can analyze using the informative menu',
            disable_notification=True)
    elif message.text == '🌍 Back':
        await bot.send_message(message.from_user.id, 'Analyze the market', reply_markup=nav.scene_analyze)
    elif message.text == '🌍 Analysis patterns':
        await bot.send_message(message.from_user.id, config.url_p)
    elif message.text == '🔔 Subscribe':
        await bot.send_message(message.from_user.id, '/subscribe')
    elif message.text == '😡 Unsubscribe':
        await bot.send_message(message.from_user.id, '/unsubscribe')
    elif message.text == '🔍 Search signals':
        is_check = True
        await bot.send_message(message.from_user.id, 'In this scene, we parse information about '
                                                     'the change in the price of bitcoin. We will '
                                                     'send you a signal and you will be the first '
                                                     'to buy or sell cryptocurrency.',
                               reply_markup=nav.scene_signals)
    elif message.text == '◀️Back':
        await bot.send_message(message.from_user.id, '✔', reply_markup=nav.main_menu)
    if db.subscriber_exists(message.from_user.id) and is_check:
        loop = asyncio.get_event_loop()
        loop.create_task(checking_info(5))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
