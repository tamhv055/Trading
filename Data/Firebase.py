import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import exceptions
import json
import time
import ExportTxt
import sys 
sys.path.insert(1, "D:\project Binance")  


import config


#https://www.freecodecamp.org/news/how-to-get-started-with-firebase-using-python/
#https://morioh.com/p/a593f973aff0



""" cred = credentials.Certificate("D:\project Binance\Data\Firebasetradedata.json")
firebase_admin.initialize_app(cred,
{'databaseURL':'https://tradedata-2734a-default-rtdb.asia-southeast1.firebasedatabase.app/'}
) """

try: 
	cred = credentials.Certificate("D:\project Binance\Data\Firebasetradedata.json")
	firebase_admin.initialize_app(cred,
		{'databaseURL':'https://tradedata-2734a-default-rtdb.asia-southeast1.firebasedatabase.app/'}
		)
except exceptions as e:
	print(e)
else:
	print("Success connect Firebase")

timestr = time.strftime("%d-%m-%Y----%H-%M-%S")

""" datatestTrading = {
	"Time" : timestr   ,
    "BuyValue" : 3500,
    "SellValue" : 4000,  
	"Doneyet": False
	}

datatestTrade = {
	"Time" : timestr ,
    "BuyValue" : 3100,
    "SellValue" : 4000,  
	"Doneyet": True
	} """

ref_trading = db.reference('/Trading')
ref_tradingSellBuy = db.reference('/Trading/SellBuy')
ref_tradingBuySell = db.reference('/Trading/BuySell')


ref_tradeyet= db.reference('/TradeDone')
""" ref_tradeyetSellBuy= db.reference('/TradeDone/SellBuy')
ref_tradeyetBuySell= db.reference('/TradeDone/BuySell') """


def AddnewTrading(data):
	# thêm log và bắt lỗi except
	ref_trading.push(data)   


def AddnewTradingSellBuy(data):
	# thêm log và bắt lỗi except
	ref_tradingSellBuy.push(data)


def AddnewTradingBuySell(data):
	# thêm log và bắt lỗi except
	ref_tradingBuySell.push(data)


def UpdateTradeSellBuySuccessFull():
	trading = ref_tradingSellBuy.get()
	timestr = time.strftime("%d-%m-%Y")
	for key, value in trading.items():
		if(value["Doneyet"] == True):
			# chuyển success trade sang tradedone
			db.reference('/TradeDone/'+timestr+'/SellBuy').push(value)
			# delete trade done
			db.reference('/Trading/SellBuy').child(key).set({})


def UpdateTradeBuySellSuccessFull():
	trading = ref_tradingBuySell.get()
	timestr = time.strftime("%d-%m-%Y")

	for key, value in trading.items():
		if(value["Doneyet"] == True):
			# chuyển success trade sang tradedone
			db.reference('/TradeDone/'+timestr+'/BuySell').push(value)
			# delete trade done
			db.reference('/Trading/BuySell').child(key).set({})


def updateTradingSellBuyDoneYet_OnlistTrading(keyTrade,price):
	try:
		for key, value in db.reference('/Trading/SellBuy').get().items():
			if(key==keyTrade):
				db.reference('/Trading/SellBuy').child(keyTrade).update({'Doneyet' : True})
				db.reference('/Trading/SellBuy').child(keyTrade).update({'BuyValue' : price})
	except exceptions as e:
		print(e)
	else:
		print('Update Trading SellBuy data')


def updateTradingBuySellDoneYet_OnlistTrading(keyTrade,price):
	try:
		for key, value in db.reference('/Trading/BuySell').get().items():
			if(key==keyTrade):
				db.reference('/Trading/BuySell').child(keyTrade).update({'Doneyet' : True})
				
				db.reference('/Trading/BuySell').child(keyTrade).update({'SellValue' : price})
	except exceptions as e:
		print(e)
	else:
		print('Update Trading BuySell data')


def getListTrading():
	try:
		listTrading = ref_trading.get()
	except exceptions as e:
		print(e)
	else:
		return listTrading


def getListSellBuyTrading():
	try:
		listTrading = ref_tradingSellBuy.get()
	except exceptions as e:
		print(e)
	else:
		return listTrading


def getListBuySellTrading():
	try:
		listTrading = ref_tradingBuySell.get()
	except exceptions as e:
		print(e)
	else:
		return listTrading




def FindBuyMaxInListBuySell():
	listBuySell = getListBuySellTrading()
	#print(listBuySell)

	listkey = [x for x in listBuySell]
	listid = [listBuySell[x]['BuyValue'] for x in listBuySell]
	#print(listid)
	maxBuyValue = max(listBuySell[x]['BuyValue'] for x in listBuySell)
	#print(maxBuyValue)
	#print(listid.index(maxBuyValue))
	key = listkey[listid.index(maxBuyValue)]
	#print(listkey[listid.index(maxBuyValue)])
	#print(listBuySell[listkey[listid.index(maxBuyValue)]])
	return key,maxBuyValue

def FindSellMinInListBuySell():
	listSellBuy = getListSellBuyTrading()
	#print(listSellBuy)
	listkey = [x for x in listSellBuy]
	listid = [listSellBuy[x]['SellValue'] for x in listSellBuy]

	minSellValue = min(listSellBuy[x]['SellValue'] for x in listSellBuy)
	key = listkey[listid.index(minSellValue)]
	return key,minSellValue

def backupDataFirebase():
    try:
        data = getListTrading()
        ExportTxt.writeDataNow(data)
    except:
        print('Error backup date Firebase')

def getQuantityBuySellwithKey(key):
	try:
		Quantity = db.reference('/Trading/BuySell').child(key).get()["Quantity"]
	except:
		print("Error getQuantityBuySellwithKey")
	return Quantity


def getQuantitySellBuywithKey(key):
	try:
		Quantity = db.reference('/Trading/SellBuy').child(key).get()["Quantity"]
	except:
		print("Error getQuantityBuySellwithKey")
	return Quantity

def check_limit_balance_Coin():
	listsellbuy = getListSellBuyTrading()
	totalcoin = sum([listsellbuy[x]['Quantity'] for x in listsellbuy])
	if totalcoin + config.TRADE_QUANTITY <= config.Limit_balance_Coin:
		return True
	else:
		return False
	
def check_limit_balance_Fiat(price):

	listbuysell = getListBuySellTrading()
	totalFiat = sum([listbuysell[x]['Quantity']*listbuysell[x]['BuyValue'] for x in listbuysell])
	if totalFiat + config.TRADE_QUANTITY*price <= config.Limit_balance_Fiat:
		return True
	else:
		return False



def Get_list_tradeDoneBuySellAday(timestr):
	try:
		listtradeDone = db.reference('/TradeDone/'+timestr+'/BuySell').get()
	except:
		print("Error listtradedoneAday")
	return listtradeDone


def Get_list_tradeDoneSellBuyAday(timestr):
	try:
		listtradeDone = db.reference('/TradeDone/'+timestr+'/SellBuy').get()
	except:
		print("Error listtradedoneAday")
	return listtradeDone



def Get_list_tradeDone():
	try:
		listtradeDone = ref_tradeyet.get()
	except:
		print("Error listtradedone")
	return listtradeDone



""" print(Get_list_tradeDoneAday('02-01-2022')) """
""" print(check_limit_balance_Fiat(4000))
keytest='-MsG6ZeazsS9Kezs9AYT'
"""
#print(getQuantityBuySellwithKey(keytest))

#AddnewTrading(datatestTrading)
#AddnewTrade()

#updateTradingDoneYet(keytest)

####Save data

### save data from file json
""" with open("book_info.json", "r") as f:
	file_contents = json.load(f)
ref.set(file_contents) """

### Push new data 
""" ref = db.reference("/Books/Best_Sellers")

with open("book_info.json", "r") as f:
	file_contents = json.load(f)

for key, value in file_contents.items():
	ref.push().set(value) """


### Update data

""" ref = db.reference("/Books/Best_Sellers/")
best_sellers = ref.get()
print(best_sellers)
for key, value in best_sellers.items():
	if(value["Author"] == "J.R.R. Tolkien"):
		value["Price"] = 90
		ref.child(key).update({"Price":80}) """


### get all Data
""" ref = db.reference('boxes')
print(ref.get()) """

### get data Query 





### Delete Data

""" ref = db.reference("/Books/Best_Sellers")

for key, value in best_sellers.items():
	if(value["Author"] == "J.R.R. Tolkien"):
		ref.child(key).set({}) """
        