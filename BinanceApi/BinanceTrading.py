import websocket, json, pprint, numpy
import config
from binance.client import BaseClient, Client
from binance.enums import *
from binance.exceptions import BinanceAPIException, BinanceOrderException, BinanceRequestException
import logging
import sys
sys.path.insert(1, "D:\project Binance\Bot_telegram")



try:
    client = Client(config.API_KEY,config.API_SECRET)
except BinanceAPIException as e:
    logging.error("BinanceAPi Error code 16: " + str(e))
    
else:
    logging.info("connect success Binance")
    #print("connect success")


def sellLimitBinance(_symbol,_quantity,_price):
    try:
        if config.EnableBinanceApi == True:
            order = client.order_limit_sell(symbol=_symbol,quantity=_quantity,price=_price)
        #print(order)
    except BinanceOrderException as e:
        logging.error("BinanceAPi code 24:" + str(e) )
        #print(e)
    else:
        logging.info("order sell success:"+"\nQuantity: "+ str(_quantity)+ "  price: " +str(_price)+ "\n" )
        #print("order sell success")


def buyLimitBinance(_symbol,_quantity, _price):
    try:
        if config.EnableBinanceApi == True:
            orderbuy= client.order_limit_buy(symbol=_symbol,quantity=_quantity,price=_price,)

    except BinanceAPIException as e:
        logging.error("BinanceAPi code 37:" + str(e) )
    else:
        logging.info("order buy success:"+"\nQuantity: "+ str(_quantity)+ "  price: " +str(_price)+ "\n" )
        #print('order buy success')


def sellMarketBinance(_symbol,_quantity,_price):
    try:
        if config.EnableBinanceApi == True:
            order = client.order_market_sell(symbol=_symbol,quantity=_quantity)
        #print(order)
    except BinanceOrderException as e:
        logging.error("BinanceAPi code 49:" + str(e) )
    else:
        logging.info("order sell success:"+"\nQuantity: "+ str(_quantity)+ "  price: " +str(_price)+ "\n" )
        #print("order sell success")


def buyMarketBinance(_symbol,_quantity,_price):
    try:
        if config.EnableBinanceApi == True:
            orderbuy= client.order_market_buy(symbol=_symbol,quantity=_quantity)
    except BinanceAPIException as e:
        logging.error("BinanceAPi code 60:" + str(e) )
    else:
        logging.info("order buy success:"+"\nQuantity: "+ str(_quantity)+ "  price: " +str(_price)+ "\n" )
        #print('order buy success')



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