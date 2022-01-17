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
######################################################
#                        Getdata                     #
######################################################
def get_balance(coinsymbol):
    try:
        balanceETH= client.get_asset_balance(asset=coinsymbol)
    except BinanceAPIException as e:
        logging.error(" BinanceTrading error code 75: " + str(e))
    return float(balanceETH["free"])

def get_balance_Coin_Free(coin):
    try:
        balanceETH= client.get_asset_balance(asset=coin)
    except BinanceAPIException as e:
        logging.error("BinanceTrading error code 82: " + str(e))
    return float(balanceETH["free"])

def get_balance_USDT_Free(Usd):
    try:
        balanceUSDT= client.get_asset_balance(asset=Usd)   
    except BinanceAPIException as e:
        logging.error("BinanceTrading error code 89: " + str(e))
    return float((balanceUSDT["free"]))



def get_fee_buy(_symbol):
    try:
        feeETHUSDT = client.get_trade_fee(symbol=_symbol)
    except BinanceAPIException as e:
        logging.error("BinanceTrading error code 98: " + str(e))
    return float(feeETHUSDT[0]['makerCommission'])

def get_fee_sell(_symbol):
    try:
        feeETHUSDT = client.get_trade_fee(symbol=_symbol)
    except BinanceAPIException as e:
        logging.error("BinanceTrading error code 105: " + str(e))
    return float(feeETHUSDT[0]['takerCommission'])

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