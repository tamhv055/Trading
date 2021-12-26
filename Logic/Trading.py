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

updateData = True

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
def buy(price,_stepjump):
    #tao lenh mua vô binance, check USDT còn không
    #BinanceTrading.buyBinance(TRADE_SYMBOL,TRADE_QUANTITY,price)

    #BinanceTrading.buyMarketBinance(TRADE_SYMBOL,TRADE_QUANTITY)
    timestr = time.strftime("%d-%m-%Y----%H-%M-%S")
    #Thêm dữ liệu lên firebase
    dataBuy = {
	        "Time" : timestr ,
            "BuyValue" : price,
            "Quantity" : TRADE_QUANTITY,
            "SellFuture" : (price*(1+feeSellPercent+feeBuyPercent+0.001)+_stepjump) ,
	        "Doneyet": False
	}
    Firebase.AddnewTradingBuySell(dataBuy)
    global updateData
    updateData = True

def sell(price,_stepjump):
    #tao lenh market bán ra binance, check ETH còn không
    #BinanceTrading.sellBinance(TRADE_SYMBOL,TRADE_QUANTITY,price)
    #BinanceTrading.sellMarketBinance(TRADE_SYMBOL,TRADE_QUANTITY)
    timestr = time.strftime("%d-%m-%Y----%H-%M-%S")
    #Thêm dữ liệu lên firebase
    dataSell = {
	            "Time" : timestr   ,
                "SellValue" : price,
                "Quantity" : TRADE_QUANTITY,
                "BuyFuture" : (price*(1-feeSellPercent-feeBuyPercent-0.001)- _stepjump) ,
	            "Doneyet": False
	            }
    Firebase.AddnewTradingSellBuy(dataSell)
    global updateData
    updateData = True

def tradingwithlistNoValue():

    #timestr = time.strftime("%d-%m-%Y----%H-%M-%S")
    safepoint= GetData.CalCulator_safepoint(TRADE_SYMBOL,Client.KLINE_INTERVAL_1MINUTE,250) 
    StepJump = GetData.Calculator_Stepjump(TRADE_SYMBOL,Client.KLINE_INTERVAL_1MINUTE,20)
    #price5min = float(GetData.average_price_5mins_ETH(TRADE_SYMBOL))
    
    realtime_priceETH = float(GetData.recent_price_ETH(TRADE_SYMBOL))
    balanceCoin = 1
    balanceUSDT = 5000
    
    """ balanceCoin = float(GetData.get_balance_ETH_Free())
    balanceUSDT = float(GetData.get_balance_USDT_Free()) """

    if realtime_priceETH > safepoint:

        if balanceUSDT> float(TRADE_QUANTITY*realtime_priceETH) :
            buy(realtime_priceETH,StepJump)
        else:
             print("No balance Coin and USDT")
        """ else:
            if balanceCoin > TRADE_QUANTITY:
                sell(realtime_priceETH) """
        
    else : #realtime_priceETH <= price5min
        if balanceCoin > TRADE_QUANTITY:
            sell(realtime_priceETH,StepJump)
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
    global updateData
    updateData = True

def SellBuyCoupleDone(_price,keytrade):
    #BinanceTrading.buyMarketBinance(TRADE_SYMBOL,TRADE_QUANTITY)
    timestr = time.strftime("%d-%m-%Y----%H-%M-%S")
    #Thêm dữ liệu lên firebase
    Firebase.updateTradingSellBuyDoneYet_OnlistTrading(keyTrade=keytrade,price=_price)
    Firebase.UpdateTradeSellBuySuccessFull()
    global updateData
    updateData = True

def buynewSlow(price,stepjump,listBuySell):
    while True:
        if price*(feeBuyPercent+feeSellPercent) < stepjump:
            stepjump = price*(feeBuyPercent+feeSellPercent)

        #listBuySell= Firebase.getListBuySellTrading()
        if listBuySell is None:
            buy(price,stepjump)
            return
            
        else : #listBuySell is not none
            # giá tăng nhẹ ,mua từ từ 
            listvalue = sorted([listBuySell[x]['BuyValue'] for x in listBuySell])
            lastvalue = listvalue[len(listvalue)-1]
            firstvalue = listvalue[0]

            # check giá trị cuối cùng của list, nếu phù hợp thì mua
            if firstvalue > price and price <= (firstvalue-stepjump) :
                buy(price,stepjump)
                return 

            if lastvalue < price and price >= (lastvalue+stepjump):
                buy(price,stepjump)
                return

            elif lastvalue > price:
               
                for i in range(len(listvalue)-1):
                    if listvalue[i]< price and price < listvalue[i+1] and  ( listvalue[i+1]-listvalue[i] ) >= (stepjump*2):
                        buy(price,stepjump)
                        return 
                    else: 
                        return
            
            else: 
                return
            
            
        
        return
            
def BuySellDone(price,stepjump,listBuySell):
    while True:
        #listBuySell= Firebase.getListBuySellTrading()
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

                    ### hàm mua bán bất đồng bộ ở đây
                    BuySellCoupleDone(_price=price,keytrade=key)
            
        break
                            
def sellnewSlow(price,stepjump,listSellBuy):
    while True:

        if price*(feeBuyPercent+feeSellPercent) < stepjump:
            stepjump = price*(feeBuyPercent+feeSellPercent)

        #listSellBuy= Firebase.getListSellBuyTrading()
        if listSellBuy is None:
            sell(price,stepjump)
            return
            
        else : #listSellBuy is not none
            # giá giảm nhẹ, bán từ từ 
            listvalue =sorted([listSellBuy[x]['SellValue'] for x in listSellBuy],reverse=True)
            lastvalue =listvalue[len(listvalue)-1]
            firstvalue = listvalue[0]

            # check giá trị cuối cùng của list, nếu phù hợp thì bán
            if firstvalue < price and price >= (firstvalue+stepjump) :
                sell(price,stepjump)
                return 

            if lastvalue > price and price <= (lastvalue-stepjump):
                sell(price,stepjump)
                return

            elif lastvalue < price:
                for i in range(len(listvalue)-1):
                    if listvalue[i]> price and price > listvalue[i+1] and  ( listvalue[i]-listvalue[i+1] ) >= (stepjump*2):
                        sell(price,stepjump)
                        return
                    else:
                        return
            
            else:
                return

            
               
        return

def SellBuyDone(price,stepjump,listSellBuy):
    while True:
        #listSellBuy= Firebase.getListSellBuyTrading()
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



def tradingwithlistHasValue(listBuySell,listSellBuy):
    
    realtime_priceETH = GetData.recent_price_ETH(TRADE_SYMBOL)
    StepJump = GetData.Calculator_Stepjump(TRADE_SYMBOL,Client.KLINE_INTERVAL_1MINUTE,20)
    print(StepJump)
    
    safepoint = GetData.CalCulator_safepoint(TRADE_SYMBOL,Client.KLINE_INTERVAL_1MINUTE,250)
    if realtime_priceETH >= safepoint:
        print("buynewSlow")
        sellnewSlow(realtime_priceETH,StepJump,listSellBuy)
        #print("BuySellDone")
        #BuySellDone(realtime_priceETH,StepJump)
        

    elif realtime_priceETH <= safepoint:
        print("sellnewSlow")
        
        buynewSlow(realtime_priceETH,StepJump,listBuySell)
        #print("SellBuyDone")
        #SellBuyDone(realtime_priceETH,StepJump)


    print("BuySellDone")
    BuySellDone(realtime_priceETH,StepJump,listBuySell)
    print("SellBuyDone")
    SellBuyDone(realtime_priceETH,StepJump,listSellBuy)


###########################################################

def TradeAllTime():

    global updateData
   
    while True: 
        if updateData == True :
            listTrading= Firebase.getListTrading()
            listBuySell= Firebase.getListBuySellTrading()
            listSellBuy= Firebase.getListSellBuyTrading()
            
            updateData = False
            
            print("Run Update listtrading")

        starttime = round(time.time()*1000)
        print(listTrading)
        
        if listTrading is None:
            print('Len list trading 0')
            tradingwithlistNoValue()
            endtime = round(time.time()*1000)
            print("time a trading work: %s ms" %(endtime-starttime))
            continue
            
        else:
            
            tradingwithlistHasValue(listBuySell,listSellBuy)
            endtime = round(time.time()*1000)
            print("time a trading work: %s ms" %(endtime-starttime))
            print('len list trading 0' )
            continue



""" def tradingListBuySellSlow():
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
            continue """