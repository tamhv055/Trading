from binance.client import Client, BaseClient
from binance.enums import *
from binance.exceptions import BinanceAPIException
import time
from Data import GetData
from Data import Firebase

import sys
sys.path.insert(1, "D:\project Binance")  
sys.path.insert(1, "D:\project Binance\Data")  

starttime = round(time.time()*1000)

timestr = time.strftime("%d-%m-%Y----%H-%M-%S")
TRADE_SYMBOL = 'ETHUSDT'
TRADE_QUANTITY = 0.005

# xem số dư tài khoản của các loại coin
balanceCoin = GetData.get_balance_ETH_Free()
balanceUSDT = GetData.get_balance_USDT_Free()

# 
realtime_priceETH = GetData.recent_price_ETH()


print(realtime_priceETH)
print(balanceUSDT)

endtime = round(time.time()*1000)
print(starttime)
print(endtime)
print("this trade work %s ms" %(endtime-starttime))

#print(GetData.get_open_price('ETHUSDT',Client.KLINE_INTERVAL_1DAY,-5))