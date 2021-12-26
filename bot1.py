import sys
sys.path.insert(1, "D:\project Binance")  
sys.path.insert(1, "D:\project Binance\Data")  
sys.path.insert(1, "D:\project Binance\BinanceApi")
sys.path.insert(1, "D:\project Binance\Logic")
sys.path.insert(1, "D:\project Binance\LogFile")

from binance.client import Client, BaseClient
from binance.enums import *
from binance.exceptions import BinanceAPIException
import json
import time
from Data import GetData
from Data import Firebase
from BinanceApi import BinanceTrading
from Logic import Trading
import config
import urllib.request
import socket
import os
from LogFile import Writelog


def internet_on():
    try:
        urllib.request.urlopen('https://www.binance.com', timeout=1)
        return True
    except socket.timeout as err: 
        return False



Trading.TradeAllTime()





#timestr = time.strftime("%d-%m-%Y----%H-%M-%S")

""" def TradeAllTime():
    
    while True: 
        listTrading= Firebase.getListTrading()
        starttime = round(time.time()*1000)
        print(listTrading)
        
        if listTrading is None:
            print('Len list trading 0')
            Trading.tradingwithlistNoValue()
            endtime = round(time.time()*1000)
            print("time a trading work: %s ms" %(endtime-starttime))
            continue
            
        else:
            
            Trading.tradingwithlistHasValue()
            endtime = round(time.time()*1000)
            print("time a trading work: %s ms" %(endtime-starttime))
            print('len list trading 0' )
            continue """

        








""" starttime = round(time.time()*1000)
endtime = round(time.time()*1000)
print("time a trading work: %s ms" %(endtime-starttime)) """



#print(GetData.get_open_price('ETHUSDT',Client.KLINE_INTERVAL_1DAY,5))