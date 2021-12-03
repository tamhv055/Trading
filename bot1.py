from binance.client import Client, BaseClient
from binance.enums import *
from binance.exceptions import BinanceAPIException
import json
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

# Lấy giá ETH tại thời điểm hiện tại
realtime_priceETH = GetData.recent_price_ETH()
endtime = round(time.time()*1000)

# Lấy các giá trị cần phân tích
highpriceinMonth = GetData.get_high_price(TRADE_SYMBOL,Client.KLINE_INTERVAL_1MONTH,1)

listTrading= Firebase.getListTrading()

print(len(listTrading))
print(listTrading)

if len(listTrading) == 0:
    print('len list trading 0')
    
    
elif len(listTrading) >0:
    print('len' )

else:
    print("len list trading error ")




print("time a trading work: %s ms" %(endtime-starttime))



#print(GetData.get_open_price('ETHUSDT',Client.KLINE_INTERVAL_1DAY,-5))