from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# --------Back button -----------
btn_back_to_main = KeyboardButton('👀 Menu')

# --------Main menu---------
btn_crypto = KeyboardButton('🤑 Cryptocurrency price')
btn_check_sign = KeyboardButton('🔍 Search signals')
btn_analytics = KeyboardButton('📈 Analyze the market')
main_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_crypto, btn_analytics, btn_check_sign)

# --------Scene crypto info about price----------'ETH', 'BTC', 'BNB', 'USDT', 'SOL'
btn_btc = KeyboardButton('₿ Bitcoin price')
btn_eth = KeyboardButton('🌈 Ethereum price')
btn_bnb = KeyboardButton('🦄 Binance coin')
btn_usdt = KeyboardButton('💩 Tether price')
btn_sol = KeyboardButton('⚡ Solana price')
scene_crypto = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_btc, btn_eth,
                                                             btn_bnb, btn_usdt, btn_sol, btn_back_to_main)

# --------Scene interval----------'ETH', 'BTC', 'BNB', 'USDT', 'SOL'
btn_hours_5 = KeyboardButton('5 hours')
btn_hours_10 = KeyboardButton('10 hours')
btn_hours_15 = KeyboardButton('15 hours')
btn_hours_30 = KeyboardButton('30 hours')
btn_back_to_analyse = KeyboardButton('🌍 Back')
scene_time = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_hours_5, btn_hours_10,
                                                              btn_hours_15, btn_hours_30,
                                                              btn_back_to_analyse)

# --------Scene crypto info chart----------'ETH', 'BTC', 'BNB', 'USDT', 'SOL'
btn_btc_analyze = KeyboardButton('₿ Bitcoin chart')
btn_eth_analyze = KeyboardButton('🌈 Ethereum chart')
btn_ada_analyze = KeyboardButton('🦄 Cardano chart')
btn_sol_analyze = KeyboardButton('⚡ Solana chart')
btn_crypto_info = KeyboardButton('🌍 Analysis patterns')
scene_analyze = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_btc_analyze, btn_eth_analyze,
                                                              btn_ada_analyze, btn_sol_analyze,
                                                              btn_crypto_info, btn_back_to_main)

# --------Scene for checking signal (buy/sell) ---------
btn_subscribe = KeyboardButton('🔔 Subscribe')
btn_unsubscribe = KeyboardButton('😡 Unsubscribe')
btn_back = KeyboardButton('◀️Back')
scene_signals = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_subscribe, btn_unsubscribe, btn_back)