from unicorn_binance_websocket_api.unicorn_binance_websocket_api_manager import BinanceWebSocketApiManager
import pyrebase
import json
import logging

config = {
    # "apiKey": "AIzaSyCU9JP2yixeKjw3NE30Pb0I0D0UQjV94gA",
    # "authDomain": "kiteconnect-stock.firebaseapp.com",
    # "databaseURL": "https://kiteconnect-stock-default-rtdb.firebaseio.com",
    # "projectId": "kiteconnect-stock",
    # "storageBucket": "kiteconnect-stock.appspot.com",
    # "messagingSenderId": "981866107803",
    # "appId": "1:981866107803:web:568ffc6b464656a6f4c73e",
    # "measurementId": "G-9BRWTZYS5C"

    "apiKey": "AIzaSyCx_6QoP5gmo2uJ_5lCfpXdQGdhQhgujhc",
    "authDomain": "binance-pro-532d6.firebaseapp.com",
    "databaseURL": "https://binance-pro-532d6-default-rtdb.firebaseio.com",
    "projectId": "binance-pro-532d6",
    "storageBucket": "binance-pro-532d6.appspot.com",
    "messagingSenderId": "875445033298",
    "appId": "1:875445033298:web:ddc349159a0ae87a0f828b"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
logging.basicConfig(level=logging.DEBUG)

binance_websocket_api_manager = BinanceWebSocketApiManager(exchange="binance.com")
# binance_websocket_api_manager.create_stream(['trade'], ['bnbbusd', 'btcusdt', 'bnbbtc'])
binance_websocket_api_manager.create_stream(['trade'],
                                            ['btcbusd', 'ethbusd', 'usdtbusd', 'bnbbusd', 'adabusd', 'dogebusd',
                                             'xrpbusd', 'usdcbusd', 'dotbusd', 'unibusd'])

a = {}
updated_times = 0
while True:

    oldest_stream_data_from_stream_buffer = binance_websocket_api_manager.pop_stream_data_from_stream_buffer()

    if oldest_stream_data_from_stream_buffer:
        q = json.loads(oldest_stream_data_from_stream_buffer)

        if q:

            if q.get('data'):
                a[q['data'].get('s')] = q['data']
                updated_times = updated_times + 1


    # print("data:", a)

    database.update({"updated_time" : updated_times})
    database.update({"Stock": a})

# period= 2 year -- interval= 1 h --
# period= 5-10 year -- interval= 1 d --

# EXAMPLE-
# {
#   "e": "trade",     // Event type
#   "E": 123456789,   // Event time
#   "s": "BNBBTC",    // Symbol
#   "t": 12345,       // Trade ID
#   "p": "0.001",     // Price
#   "q": "100",       // Quantity
#   "b": 88,          // Buyer order Id
#   "a": 50,          // Seller order Id
#   "T": 123456785,   // Trade time
#   "m": true,        // Is the buyer the market maker?
#   "M": true         // Ignore.
# }
