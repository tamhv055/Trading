import websocket, json, pprint, numpy
import config
from binance.client import BaseClient, Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException, BinanceRequestException


try:
    client = Client(config.API_KEY,config.API_SECRET)
except BinanceAPIException as e:
    print(e)
else:
    print("connect success")


def sellLimitBinance(_symbol,_quantity,_price):
    try:
        order = client.order_limit_sell(symbol=_symbol,quantity=_quantity,price=_price)
        #print(order)
    except BinanceOrderException as e:
        print(e)
    else:
        print("order sell success")


def buyLimitBinance(_symbol,_quantity, _price):
    try:
        orderbuy= client.order_limit_buy(symbol=_symbol,quantity=_quantity,price=_price,)
        print(orderbuy)
    except BinanceAPIException as e:
        print(e)
    else:
        print('order buy success')


def sellMarketBinance(_symbol,_quantity):
    try:
        order = client.order_market_sell(symbol=_symbol,quantity=_quantity)
        #print(order)
    except BinanceOrderException as e:
        print(e)
    else:
        print("order sell success")


def buyMarketBinance(_symbol,_quantity):
    try:
        orderbuy= client.order_market_buy(symbol=_symbol,quantity=_quantity)
        print(orderbuy)
    except BinanceAPIException as e:
        print(e)
    else:
        print('order buy success')



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

"""""