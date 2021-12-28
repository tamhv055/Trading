from binance.client import Client,BaseClient
from binance.exceptions import BinanceAPIException

import sys
sys.path.insert(1, "D:\project Binance") 
sys.path.insert(1, "D:\project Binance\Data")
import ExportTxt
import config


try:
    client = Client(config.API_KEY,config.API_SECRET)
except BinanceAPIException as e:
    print(e)
else:
    print("connect success")



def recent_price_ETH(_symbol):
    price = client.get_recent_trades(symbol=_symbol,limit=1)
    return float(price[0]["price"])

def average_price_5mins(_symbol):
    avg_price = client.get_avg_price(symbol=_symbol)
    return float(avg_price['price'])

def get_balance(coinsymbol):
    balanceETH= client.get_asset_balance(asset=coinsymbol)
    return float(balanceETH["free"])

def get_balance_ETH_Free():
    balanceETH= client.get_asset_balance(asset=config.Coin)
    return float(balanceETH["free"])

def get_balance_USDT_Free():
    balanceUSDT= client.get_asset_balance(asset=config.Usd)   
    return float((balanceUSDT["free"]))



def get_fee_buy(_symbol):
    feeETHUSDT = client.get_trade_fee(symbol=_symbol)
    return float(feeETHUSDT[0]['makerCommission'])

def get_fee_sell(_symbol):
    feeETHUSDT = client.get_trade_fee(symbol=_symbol)
    return float(feeETHUSDT[0]['takerCommission'])

def get_candles(_symbol,KlineTime):
    candles = client.get_klines(symbol=_symbol, interval=KlineTime)
    return candles

def get_open_price(_symbol,KlineTime,count):
    list_open_price=[]
    candles = client.get_klines(symbol=_symbol, interval=KlineTime)
    #candles have 500 element, but we have get "Count" element with Candles[count:]
    #print(candles[count:])
    for x in candles[(0-count):]:
        #print(x)
        #print(x[1])
        list_open_price.append(float(x[1]))
    return list_open_price

def get_close_price(_symbol,KlineTime,count):
    list_close_price=[]
    candles = client.get_klines(symbol=_symbol, interval=KlineTime) 
    for x in candles[(0-count):]:
        list_close_price.append(float(x[4]))

    return list_close_price

def get_high_price(_symbol,KlineTime,count):
    list_high_price=[]
    candles = client.get_klines(symbol=_symbol, interval=KlineTime) 
    for x in candles[(0-count):]:
        list_high_price.append(float(x[2]))

    return list_high_price

def get_low_price(_symbol,KlineTime,count):
    list_low_price=[]
    candles = client.get_klines(symbol=_symbol, interval=KlineTime) 
    for x in candles[(0-count):]:
        list_low_price.append(float(x[3]))

    return list_low_price

def Calculator_Average_Listprice(list_price:list):
    len_list  = len(list_price)
    sum_price = sum(list_price)
    return float(sum_price/len_list)

def CalCulator_safepoint(_symbol,KlineTime,count):
    list_low = get_low_price(_symbol,KlineTime,count)
    
    Low_Average = Calculator_Average_Listprice(list_low)
    
    list_high = get_high_price(_symbol,KlineTime,count)
    
    High_Average = Calculator_Average_Listprice(list_high)
    
    return float((Low_Average+High_Average)/2)

def Calculator_Stepjump(_symbol,KlineTime,count):

    list_low = get_low_price(_symbol,KlineTime,count)

    list_high = get_high_price(_symbol,KlineTime,count)

    return float((sum(list_high)-sum(list_low))/count)

def Calculator_SpeedJump(_symbol,count):
    if count > 2:
        sum= 0
        list_price_recent = client.get_recent_trades(symbol=_symbol,limit=count)
        for i in range(len(list_price_recent)-1):
            sum = sum + (list_price_recent[i+1]-list_price_recent[i])

        SpeedJump = sum/len(list_price_recent)
    return SpeedJump


def check_negative(s):
    try:
        f = float(s)
        if (f < 0):
            return True
        # Otherwise return false
        return False
    except ValueError:
        return False

def Count_Pos_And_Negg_List(_symbol,count): # 500
    
    if count > 2:
        Positive = 0
        Negative = 0
        list_price_recent = client.get_recent_trades(symbol=_symbol,limit=count)
        for i in range(len(list_price_recent)-1):
            if check_negative(list_price_recent[i+1]-list_price_recent[i]) == True:
                Negative = Negative+1
            else:
                Positive = Positive+1

        
    return Positive,Negative


#print(Count_Pos_And_Negg_List('ETHUSDT',50))


""" print(recent_price_ETH())
print(average_price_5mins_ETH())
print(get_balance_ETH_Free())
print(get_balance_USDT_Free())
print(get_fee_buy())
print(get_fee_sell())
print(get_open_price('ETHUSDT',Client.KLINE_INTERVAL_1DAY,-5))
print(get_high_price('ETHUSDT',Client.KLINE_INTERVAL_1DAY,-5))
print(get_low_price('ETHUSDT',Client.KLINE_INTERVAL_1DAY,-5))
print(get_close_price('ETHUSDT',Client.KLINE_INTERVAL_1DAY,-5))

print(Calculator_Average_Listprice(get_open_price('ETHUSDT',Client.KLINE_INTERVAL_1DAY,-5)))

safe_point = CalCulator_safepoint('ETHUSDT',Client.KLINE_INTERVAL_1DAY,-30)
print(safe_point) """

""" depth = client.get_order_book(symbol='ETHUSDT')
trades = client.get_aggregate_trades(symbol='ETHUSDT') """

# candles = client.get_klines(symbol='ETHUSDT', interval=Client.KLINE_INTERVAL_30MINUTE)
# print(candles[-1:])
# print(len(candles))
# ExportTxt.writeDataNow(candles)

"""  [
    1499040000000,      // Open time    0
    "0.01634790",       // Open         1
    "0.80000000",       // High         2
    "0.01575800",       // Low          3
    "0.01577100",       // Close        4
    "148976.11427815",  // Volume
    1499644799999,      // Close time
    "2434.19055334",    // Quote asset volume
    308,                // Number of trades
    "1756.87402397",    // Taker buy base asset volume
    "28.46694368",      // Taker buy quote asset volume
    "17928899.62484339" // Ignore.
  ]
 """



""" #Xem giá ETHUSDT hiện tại
price = client.get_recent_trades(symbol='ETHUSDT',limit=1)
print(price[0]["price"])
 """


""" # Xem giá ETHUSDT trung bình trong 5 phút
avg_price = client.get_avg_price(symbol='ETHUSDT')
print('avg price:')
print(avg_price)
print('\n\n') """

""" #xem số dư ETH
balanceETH= client.get_asset_balance(asset='ETH')
print(balanceETH)
print(balanceETH["free"]) """

""" #xem số dư USDT
balanceUSDT= client.get_asset_balance(asset='USDT')
print(balanceUSDT)
print(balanceUSDT["free"]) """

""" #xem phí trade ETHUSDT
feeETHUSDT = client.get_trade_fee(symbol='ETHUSDT')
print(feeETHUSDT) """