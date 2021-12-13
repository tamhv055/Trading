from binance.client import Client, BaseClient
from binance.enums import *
from binance.exceptions import BinanceAPIException
import json
import time
from Data import GetData
from Data import Firebase
from BinanceApi import BinanceTrading
import sys
sys.path.insert(1, "D:\project Binance")  
sys.path.insert(1, "D:\project Binance\Data")  
sys.path.insert(1, "D:\project Binance\BinanceApi")



timestr = time.strftime("%d-%m-%Y----%H-%M-%S")
TRADE_SYMBOL = 'ETHUSDT'
TRADE_QUANTITY = 0.005
StepJump = float()
prevPoint = float()
JumpPoint = float()
nextPoint = float()
list1Minute = {}
listbuy = {}
listsell = {}


# xem số dư tài khoản của các loại coin
balanceCoin = GetData.get_balance_ETH_Free()
balanceUSDT = GetData.get_balance_USDT_Free()

# Lấy giá ETH tại thời điểm hiện tại
realtime_priceETH = GetData.recent_price_ETH(TRADE_SYMBOL)
feeBuyPercent= GetData.get_fee_buy(TRADE_SYMBOL)
feeSellPercent = GetData.get_fee_sell(TRADE_SYMBOL)




# Lấy các giá trị cần phân tích
highpriceinMonth = GetData.get_high_price(TRADE_SYMBOL,Client.KLINE_INTERVAL_1MONTH,1)

listTrading= Firebase.getListTrading()
listTradingBuySell = Firebase.getListBuySellTrading()
listTradingSellBuy = Firebase.getListSellBuyTrading()



print(len(listTrading))
#print(listTrading)


##### trading with no value in list traing 
def buy(price):
    #tao lenh mua vô binance, check USDT còn không
    #BinanceTrading.buyBinance(TRADE_SYMBOL,TRADE_QUANTITY,price)

    #Thêm dữ liệu lên firebase
    dataBuy = {
	        "Time" : timestr   ,
            "BuyValue" : price,
            "SellFuture" : price*(1+feeSellPercent+feeBuyPercent+0.002) ,
	        "Doneyet": False
	}
    Firebase.AddnewTradingBuySell(dataBuy)

def sell(price):
    #tao lenh market bán ra binance, check ETH còn không
    #BinanceTrading.sellBinance(TRADE_SYMBOL,TRADE_QUANTITY,price)

    #Thêm dữ liệu lên firebase
    dataSell = {
	            "Time" : timestr   ,
                "SellValue" : price,
                "BuyFuture" : price*(1+feeSellPercent+feeBuyPercent+0.002) ,
	            "Doneyet": False
	            }
    Firebase.AddnewTradingSellBuy(dataSell)

def tradingwithlistNoValue():

    timestr = time.strftime("%d-%m-%Y----%H-%M-%S")
    #safepoint= GetData.CalCulator_safepoint(TRADE_SYMBOL,Client.KLINE_INTERVAL_5MINUTE,50) 
    price5min = float(GetData.average_price_5mins_ETH(TRADE_SYMBOL))
    realtime_priceETH = float(GetData.recent_price_ETH(TRADE_SYMBOL))
    balanceCoin = float(GetData.get_balance_ETH_Free())
    balanceUSDT = float(GetData.get_balance_USDT_Free())

    if realtime_priceETH >price5min:
        if balanceUSDT> float(TRADE_QUANTITY*realtime_priceETH) :
            buy(realtime_priceETH)
        else:
            if balanceCoin > TRADE_QUANTITY:
                sell(realtime_priceETH)
            else:
                print("No balance Coin and USDT")
    else : #realtime_priceETH <= price5min
        if balanceCoin > TRADE_QUANTITY:
            sell(realtime_priceETH)
        else:
            if balanceUSDT> float(TRADE_QUANTITY*realtime_priceETH):
                buy(realtime_priceETH)
            else: 
                print("No balance Coin and USDT")
###########################################################


###########################################################

# Trading with have list trading
def SellBuyDone(dataBuy):
    #tao lenh mua vô binance, check USDT còn không
    #BinanceTrading.buyBinance(TRADE_SYMBOL,TRADE_QUANTITY,price)

    #Thêm dữ liệu lên firebase
    Firebase.updateTradingSellBuyDoneYet(dataBuy.get)


def tradingListBuySell():
    while True:
        listBuySell= Firebase.getListBuySellTrading()
        if listBuySell is None:
            print("list no value")
            continue
        elif listBuySell > 0:
            #hàm bán list ở đây
            
            continue
        else:
            print("error List Buy Sell")
            continue


def tradingListSellBuy():
    while True:
        listSellBuy= Firebase.getListSellBuyTrading()
        if listSellBuy is None:
            print("list no value")
            continue
        elif listSellBuy > 0:
            #hàm bán list ở đây
            continue
        else:
            print("error List Buy Sell")
            continue


def tradingwithlistHasValue():
    print('ashyasd')



###########################################################

def TradeAllTime():
    while True: 
        if listTrading is None:
            print('Len list trading 0')
            tradingwithlistNoValue()
            continue
            
        elif len(listTrading) >0:

            print('len list trading 0' )
            continue

        else:
            print("len list trading error ")
            continue




starttime = round(time.time()*1000)
endtime = round(time.time()*1000)
print("time a trading work: %s ms" %(endtime-starttime))

#print(GetData.get_open_price('ETHUSDT',Client.KLINE_INTERVAL_1DAY,5))