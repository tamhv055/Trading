   
import websocket, json, pprint, numpy
import config
from binance.client import BaseClient, Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException, BinanceRequestException





list_Price_Closes = []

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"


TRADE_SYMBOL = 'ETHUSDT'
TRADE_QUANTITY = 0.005


try:
    client = Client(config.API_KEY,config.API_SECRET)
except BinanceAPIException as e:
    print(e)
else:
    print("connect success")


#Xem giá ETHUSDT hiện tại
price = client.get_recent_trades(symbol='ETHUSDT',limit=1)
print(price[0]["price"])

#
avg_price = client.get_avg_price(symbol='ETHUSDT',)
print('avg price:')
print(avg_price)
print('\n\n')

#xem số dư ETH
balanceETH= client.get_asset_balance(asset='ETH')
print(balanceETH)
print(balanceETH["free"])

#xem số dư USDT
balanceUSDT= client.get_asset_balance(asset='USDT')
print(balanceUSDT)
print(balanceUSDT["free"])

#xem phí trade ETHUSDT
feeETHUSDT = client.get_trade_fee(symbol='ETHUSDT')
print(feeETHUSDT)

# bán eth
'''try:
    order = client.order_limit_sell(symbol='ETHUSDT',quantity=0.005,price='5000')
    print(order)
except BinanceOrderException as e:
    print(e)
else:
    print("order sell success")'''

#Mua ETH
""" try:
    orderbuy= client.order_limit_buy(symbol='ETHUSDT',quantity=0.005,price='5000',)
    print(orderbuy)
except BinanceAPIException as e:
    print(e)
else:
    print('order buy success') """

#Hủy lệnh mua bán
""" try:
    cancel = client.cancel_order(symbol='ETHUSDT',orderId=6021039034)

    print(cancel)
except BinanceRequestException as e:
    print(e)
else:
    print("Cancel success") """

""" def order(side,quantity,symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print("sending order")
        #order = client.create_order(symbol=symbol,side=side,type=order_type,quantity=quantity)
        
        print(order)
        return True

    except Exception as e:
        return False

    return True

def on_open(ws):
    print('open connection')

def on_close(ws):
    print('closed connetion')


def on_message(ws,message):

    global list_Price_Closes
    print('received message :')
    json_message = json.loads(message)
    pprint.pprint(json_message)

    kline = json_message['k']
    # Kiểu tra chuỗi kết thúc hay chưa?
    is_kline_closed =  kline['x']
    # giá coin kết thúc chuỗi
    close_price = kline['c']

    if is_kline_closed:
        print("Kline closed at {}".format(close_price))
        list_Price_Closes.append(float(close_price))
        print(list_Price_Closes)

        
ws = websocket.WebSocketApp(SOCKET, on_open=on_open,on_close=on_message, on_message=on_message)

ws.run_forever() """






""" {
  "e": "kline",     // Event type
  "E": 123456789,   // Event time
  "s": "BNBBTC",    // Symbol
  "k": {
    "t": 123400000, // Kline start time
    "T": 123460000, // Kline close time
    "s": "BNBBTC",  // Symbol
    "i": "1m",      // Interval
    "f": 100,       // First trade ID
    "L": 200,       // Last trade ID
    "o": "0.0010",  // Open price
    "c": "0.0020",  // Close price
    "h": "0.0025",  // High price
    "l": "0.0015",  // Low price
    "v": "1000",    // Base asset volume
    "n": 100,       // Number of trades
    "x": false,     // Is this kline closed?
    "q": "1.0000",  // Quote asset volume
    "V": "500",     // Taker buy base asset volume
    "Q": "0.500",   // Taker buy quote asset volume
    "B": "123456"   // Ignore
  }
} """