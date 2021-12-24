import sys
sys.path.insert(1, "D:\project Binance")  
sys.path.insert(1, "D:\project Binance\Data")  
sys.path.insert(1, "D:\project Binance\BinanceApi")
from binance.client import Client, BaseClient
from binance.enums import *
from binance.exceptions import BinanceAPIException


from Data import GetData
from Data import Firebase
import time
import config





TRADE_SYMBOL = config.TRADE_SYMBOL
TRADE_QUANTITY = config.TRADE_QUANTITY

StepJump = float()
prevPoint = GetData.average_price_5mins(TRADE_SYMBOL)
nextPoint = float()

buypoint = float()
sellpoint = float()

listbuy = {}
listsell = {}


# xem số dư tài khoản của các loại coin
""" balanceCoin = 1
balanceUSDT = 5000 """
""" balanceCoin = GetData.get_balance_ETH_Free()
balanceUSDT = GetData.get_balance_USDT_Free() """

# Lấy giá ETH tại thời điểm hiện tại
realtime_priceETH = GetData.recent_price_ETH(TRADE_SYMBOL)
feeBuyPercent= GetData.get_fee_buy(TRADE_SYMBOL)
feeSellPercent = GetData.get_fee_sell(TRADE_SYMBOL)


# Lấy các giá trị cần phân tích
highpriceinMonth = GetData.get_high_price(TRADE_SYMBOL,Client.KLINE_INTERVAL_1MONTH,1)

""" listTrading= Firebase.getListTrading()
listTradingBuySell = Firebase.getListBuySellTrading()
listTradingSellBuy = Firebase.getListSellBuyTrading() """

##### trading with no value in list traing 
def buy(price):
    #tao lenh mua vô binance, check USDT còn không
    #BinanceTrading.buyBinance(TRADE_SYMBOL,TRADE_QUANTITY,price)

    #BinanceTrading.buyMarketBinance(TRADE_SYMBOL,TRADE_QUANTITY)
    timestr = time.strftime("%d-%m-%Y----%H-%M-%S")
    #Thêm dữ liệu lên firebase
    dataBuy = {
	        "Time" : timestr ,
            "BuyValue" : price,
            "Quantity" : TRADE_QUANTITY,
            "SellFuture" : price*(1+feeSellPercent+feeBuyPercent+0.002) ,
	        "Doneyet": False
	}
    Firebase.AddnewTradingBuySell(dataBuy)

def sell(price):
    #tao lenh market bán ra binance, check ETH còn không
    #BinanceTrading.sellBinance(TRADE_SYMBOL,TRADE_QUANTITY,price)
    #BinanceTrading.sellMarketBinance(TRADE_SYMBOL,TRADE_QUANTITY)
    timestr = time.strftime("%d-%m-%Y----%H-%M-%S")
    #Thêm dữ liệu lên firebase
    dataSell = {
	            "Time" : timestr   ,
                "SellValue" : price,
                "Quantity" : TRADE_QUANTITY,
                "BuyFuture" : price*(1-feeSellPercent-feeBuyPercent-0.002) ,
	            "Doneyet": False
	            }
    Firebase.AddnewTradingSellBuy(dataSell)

def tradingwithlistNoValue():

    #timestr = time.strftime("%d-%m-%Y----%H-%M-%S")
    safepoint= GetData.CalCulator_safepoint(TRADE_SYMBOL,Client.KLINE_INTERVAL_1MINUTE,250) 
    #price5min = float(GetData.average_price_5mins_ETH(TRADE_SYMBOL))
    
    realtime_priceETH = float(GetData.recent_price_ETH(TRADE_SYMBOL))
    balanceCoin = 1
    balanceUSDT = 5000
    
    """ balanceCoin = float(GetData.get_balance_ETH_Free())
    balanceUSDT = float(GetData.get_balance_USDT_Free()) """

    if realtime_priceETH > safepoint:

        if balanceUSDT> float(TRADE_QUANTITY*realtime_priceETH) :
            buy(realtime_priceETH)
        else:
             print("No balance Coin and USDT")
        """ else:
            if balanceCoin > TRADE_QUANTITY:
                sell(realtime_priceETH) """
        
    else : #realtime_priceETH <= price5min
        if balanceCoin > TRADE_QUANTITY:
            sell(realtime_priceETH)
        else: 
                print("No balance Coin and USDT")
        """ else:
            if balanceUSDT> float(TRADE_QUANTITY*realtime_priceETH):
                buy(realtime_priceETH)
             """
###########################################################


###########################################################



# Trading with have list trading
def BuySellCoupleDone(_price,keytrade):
     #BinanceTrading.sellMarketBinance(TRADE_SYMBOL,TRADE_QUANTITY)
    timestr = time.strftime("%d-%m-%Y----%H-%M-%S")
    #Thêm dữ liệu lên firebase
    Firebase.updateTradingBuySellDoneYet_OnlistTrading(keyTrade=keytrade,price=_price)
    Firebase.UpdateTradeBuySellSuccessFull()

def SellBuyCoupleDone(_price,keytrade):
    #BinanceTrading.buyMarketBinance(TRADE_SYMBOL,TRADE_QUANTITY)
    timestr = time.strftime("%d-%m-%Y----%H-%M-%S")
    #Thêm dữ liệu lên firebase
    Firebase.updateTradingSellBuyDoneYet_OnlistTrading(keyTrade=keytrade,price=_price)
    Firebase.UpdateTradeSellBuySuccessFull()


def buynewSlow(price,stepjump):
    while True:
        listBuySell= Firebase.getListBuySellTrading()
        if listBuySell is None:
            buy(price)
            break
            
        else : #listBuySell is not none
            # giá tăng nhẹ ,mua từ từ 
            listvalue = sorted([listBuySell[x]['BuyValue'] for x in listBuySell])
            lastvalue = listvalue[len(listvalue)-1]

            # check giá trị cuối cùng của list, nếu phù hợp thì mua
            if lastvalue < price and price >= (lastvalue+stepjump):
                buy(price)
                break

            elif lastvalue > price:
               
                for i in range(len(listvalue)-1):
                    if listvalue[i]< price and price < listvalue[i+1] and  ( listvalue[i+1]-listvalue[i] ) >= (stepjump*1.9):
                        buy(price)
                        break 
                    else:
                        break
            else:
                break

        break
            

def BuySellDone(price,stepjump):
    while True:
        listBuySell= Firebase.getListBuySellTrading()
        if listBuySell is not None:
            
        #listSellBuy is not none
            # giá giảm nhẹ, mua vào để hoàn thành  
            listSellFuture = [listBuySell[x]['SellFuture'] for x in listBuySell]
            #lastvalue =listBuyFuture[range(listBuyFuture)-1]

            #danh sách key on firebase
            listkey = [x for x in listBuySell]
            #danh sách thứ tự của key trên firebase 0-123 ...
            listid = [listBuySell[x]['SellFuture'] for x in listBuySell]

            ## lấy key của giá trị price
            ## key = listkey[listid.index(value)]

            for value in listSellFuture:
                if value <= price:
                    ## lấy key của giá trị value
                    key = listkey[listid.index(value)]
                    BuySellCoupleDone(_price=price,keytrade=key)
            
        break
    
                            
def sellnewSlow(price,stepjump):
    while True:
        listSellBuy= Firebase.getListSellBuyTrading()
        if listSellBuy is None:
            sell(price)
            break
            
        else : #listSellBuy is not none
            # giá giảm nhẹ, bán từ từ 
            listvalue =sorted([listSellBuy[x]['SellValue'] for x in listSellBuy],reverse=True)
            lastvalue =listvalue[len(listvalue)-1]

            # check giá trị cuối cùng của list, nếu phù hợp thì bán
            if lastvalue > price and price <= (lastvalue-stepjump):
                sell(price)
                break

            elif lastvalue < price:
                for i in range(len(listvalue)-1):
                    if listvalue[i]> price and price > listvalue[i+1] and  ( listvalue[i]-listvalue[i+1] ) >= (stepjump*1.9):
                        sell(price)
                        break 
                    else:
                        break
            else:
                break    
        break

def SellBuyDone(price,stepjump):
    while True:
        listSellBuy= Firebase.getListSellBuyTrading()
        if listSellBuy is not None:
            
        #listSellBuy is not none
            # giá tăng nhẹ, mua vào để hoàn thành  
            listBuyFuture = [listSellBuy[x]['BuyFuture'] for x in listSellBuy]
            #lastvalue =listBuyFuture[range(listBuyFuture)-1]

            #danh sách key on firebase
            listkey = [x for x in listSellBuy]
            #danh sách thứ tự của key trên firebase 0-123 ...
            listid = [listSellBuy[x]['BuyFuture'] for x in listSellBuy]

            ## lấy key của giá trị price
            ## key = listkey[listid.index(value)]

            for value in listBuyFuture:
                if value >= price:
                    ## lấy key của giá trị value
                    key = listkey[listid.index(value)]
                    SellBuyCoupleDone(_price=price,keytrade=key)

        break



def tradingwithlistHasValue():
    
    realtime_priceETH = GetData.recent_price_ETH(TRADE_SYMBOL)
    StepJump = GetData.Calculator_Stepjump(TRADE_SYMBOL,Client.KLINE_INTERVAL_1MINUTE,20)
    print(StepJump)
    safepoint = GetData.CalCulator_safepoint(TRADE_SYMBOL,Client.KLINE_INTERVAL_1MINUTE,250)
    if realtime_priceETH >= safepoint:
        print("buynewSlow")
        buynewSlow(realtime_priceETH,StepJump)
        print("BuySellDone")
        BuySellDone(realtime_priceETH,StepJump)

    elif realtime_priceETH <= safepoint:
        print("sellnewSlow")
        sellnewSlow(realtime_priceETH,StepJump)
        print("SellBuyDone")
        SellBuyDone(realtime_priceETH,StepJump)
    



###########################################################





def tradingListBuySellSlow():
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

def tradingListSellBuySlow():
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