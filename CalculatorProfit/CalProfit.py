import logging
import sys 
sys.path.insert(1, "D:\project Binance\Data") 
sys.path.insert(1, "D:\project Binance")


from Data import Firebase
from Data import GetData
import config
import time





## tính profit trade
def ProfitFiat(_SellPrice,_feeSellPercent,_BuyPrice, _feeBuyPercent,_quantity):
    try:
        profit = _quantity*(_SellPrice*(1-_feeSellPercent) -_BuyPrice*(1-_feeBuyPercent))
    except Exception as e:
        logging.error("Calprofit code 21: Error ProfitFiat"+ str(e))
        #print("Error ProfitFiat")
    return profit

    

def ProfitAday(timestr,feeSellPercent,feeBuyPercent):
    try:
        listBuySell = Firebase.Get_list_tradeDoneBuySellAday(timestr)
        listSellBuy = Firebase.Get_list_tradeDoneSellBuyAday(timestr)
        totalprofit = 0
        if listBuySell is not None:
            list = [(listBuySell[x]['Quantity'],listBuySell[x]['BuyValue'],listBuySell[x]['SellValue']) for x in listBuySell]
            totalprofit  = totalprofit + sum([ProfitFiat( x[2] ,feeSellPercent , x[1] , feeBuyPercent  , x[0] ) for x in list])

        if listSellBuy is not None:
            list = [(listSellBuy[x]['Quantity'],listSellBuy[x]['BuyValue'],listSellBuy[x]['SellValue']) for x in listSellBuy]
            totalprofit  =totalprofit + sum([ProfitFiat( x[2] ,feeSellPercent , x[1] , feeBuyPercent  , x[0] ) for x in list])
    except Exception as e:
        logging.error("CallProfit code error 40:\n" + str(e))
    return totalprofit

def ProfitAll():
    try:
        feebuy=GetData.get_fee_buy(config.TRADE_SYMBOL)
        feesell = GetData.get_fee_sell(config.TRADE_SYMBOL)
        totalprofit = 0
        listProfitDay = []
        listtradone = Firebase.Get_list_tradeDone()
        for p_id, p_info in listtradone.items():

            profitthisday = ProfitAday(p_id,feesell,feebuy)
            listProfitDay= listProfitDay + [(p_id,profitthisday)]
            totalprofit = totalprofit + profitthisday
    except Exception as e:
        logging.error("Calprofit Error code 56: " + str(e))   
    return listProfitDay,totalprofit




""" A= ProfitAll()
print(A[0])
print(A[1])
stringtext = ""
for x,y in A[0]:
        stringtext =stringtext + "Day" + str(x) + "  :" + str(y) + "  Usd \n"
        print(stringtext) """

""" feebuy=GetData.get_fee_buy(config.TRADE_SYMBOL)
feesell = GetData.get_fee_sell(config.TRADE_SYMBOL)
print(feebuy, feesell)
print( ProfitFiat (3855.78,0.001,3843.21,0,0.005))
print(ProfitAday("05-01-2022",feesell,feebuy)) """



#def Alltrade
