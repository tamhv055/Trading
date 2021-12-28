import sys
from types import prepare_class
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
            print("listbuysell:", listvalue)

            # listvalue 1 3 4 5 6 7 9
            # check giá trị cuối cùng của list, nếu phù hợp thì mua
            #Check giá trị đầu tiên để buy
            if firstvalue > price and (firstvalue-price) >= (0.9*stepjump) :
                buy(price,stepjump)
                return 
            # check giá trị cuối cùng
            elif lastvalue < price and (price-lastvalue) >= (0.9*stepjump):
                buy(price,stepjump)
                return
            # Check giá trị ở giữa
            elif firstvalue<price<lastvalue and (price-firstvalue)>=stepjump and (lastvalue-price) >= stepjump:
               
                for i in range(len(listvalue)):
                    if listvalue[i]< price < listvalue[i+1] and  (listvalue[i+1]-listvalue[i] ) >= (stepjump*2) and (listvalue[i+1]-price) >= 0.9*stepjump and  (price-listvalue[i]) >= 0.9*stepjump : 
                        buy(price,stepjump)
                        return 
                    else: 
                        return
            
            # and  ( listvalue[i+1]-listvalue[i] ) >= (stepjump*2)
            # and (listvalue[i+1]-price) >= 0.9*stepjump and (listvalue[i]-price) >= 0.9*stepjump 
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
            print("listsellbuy:", listvalue)
            firstvalue = listvalue[0]

            # listvalue  11 9 5 4 3 2 1


             # check giá trị cuối cùng của list, nếu phù hợp thì bán
             # check vị trí đầu
            if firstvalue < price and (price-firstvalue) >= (0.9*stepjump) :
                sell(price,stepjump)
                return 
            #check vị trí cuối
            elif lastvalue > price and (lastvalue-price) >= (0.9*stepjump):
                sell(price,stepjump)
                return
            #check vị trí giữa
            elif firstvalue > price > lastvalue and (firstvalue-price)>=(0.9*stepjump) and (price-lastvalue) >= (0.9*stepjump) :
                for i in range(len(listvalue)):
                    if listvalue[i]> price > listvalue[i+1] and (listvalue[i]-listvalue[i+1]) >= (stepjump*2) and (listvalue[i]-price) >= 0.9*stepjump and (price-listvalue[i+1])>= 0.9*stepjump :
                        sell(price,stepjump)
                        return
                    else:
                        return
            
            else:
                return

            # and (listvalue[i]-listvalue[i+1]) >= (stepjump*2)
            # and (listvalue[i]-price) >= 0.9*stepjump and (price-listvalue[i+1])>= 0.9*stepjump  

            """ for i in range(len(listvalue)):
                if i == 0:
                    if price > listvalue[i]: 
                        if price-listvalue[i] > (0.9*stepjump):
                            sell(price,stepjump)
                            return
                elif i == len(listvalue)-1:
                    if price < listvalue[len(listvalue)-1]:
                        if listvalue[len(listvalue)-1] - price > (0.9*stepjump):
                            sell(price,stepjump)
                            return
                else:
                    if listvalue[i]> price and price > listvalue[i+1] and (listvalue[i]-listvalue[i+1]) >= (stepjump*1.9) and (listvalue[i]-price) >= 0.9*stepjump or (price-listvalue[i+1])>= 0.9*stepjump :
                        sell(price,stepjump)
                        return """
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
        starttime = round(time.time()*1000)
        if updateData == True :
            #time.sleep(5)
            listTrading= Firebase.getListTrading()
            listBuySell= Firebase.getListBuySellTrading()
            listSellBuy= Firebase.getListSellBuyTrading()
            
            updateData = False
            
            print("Run Update listtrading")

        
        
        
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