from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import sys



sys.path.insert(1, "D:\project Binance\CalculatorProfit") 
sys.path.insert(1, "D:\project Binance\Bot_telegram")
sys.path.insert(1, "D:\project Binance\Data")
sys.path.insert(1, "D:\project Binance")



from CalculatorProfit import CalProfit
from BinanceApi import BinanceTrading
from config import Coin, Usd, TRADE_SYMBOL, TRADE_QUANTITY
from Data import Firebase
from Data import GetData



updater = Updater("5020937139:AAGfNblKv-ohgSZCabNrLmNNvopZ_Bpl7qA",
                  use_context=True)
  
UserId = "1686353548"
#updater.bot.send_message(UserId,"abasosaisadogoasdppphawd")

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to the Bot.Please write\
        /help to see the commands available.")
  
def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /balance - To get blance
    /Info_trading -  To get info trading
    /totalprofit - To get all profit
    """)
  
  
def balance(update: Update, context: CallbackContext):
    BalanceCoin = BinanceTrading.get_balance_Coin_Free(Coin)
    BalanceUSD = BinanceTrading.get_balance_USDT_Free(Usd)
    reply_text = "Balance of "+ str(Coin) + ": " + str(BalanceCoin)
    reply_text =reply_text+ "\nBalance of " + str(Usd) + ": " + str(BalanceUSD)
    
    update.message.reply_text(reply_text)
  
def Info_trading(update: Update, context: CallbackContext):
    string_text= "Info Trading now:\n"
    listBuySell = Firebase.getListBuySellTrading()
    listSellBuy = Firebase.getListSellBuyTrading()
    pricenow =GetData.recent_price_ETH(TRADE_SYMBOL)
    if listBuySell is not None:
        countBuySell = len(listBuySell)
        print(countBuySell)
        usedUSD = 0
        Sellnow = 0 
        for x in listBuySell:
            usedUSD= usedUSD +  listBuySell[x]["BuyValue"]*listBuySell[x]["Quantity"]
            Sellnow = Sellnow + pricenow*listBuySell[x]["Quantity"]

        profitnow = Sellnow - usedUSD
        string_text = string_text + "List Buy Sell : "+ str(countBuySell) + " Trade use " +  str(round(usedUSD,3)) +" "+ str(Usd) + " \n"
        string_text =  string_text + "If Sell all now, we will lose :  " + str(round(profitnow,3)) +" "+ str(Usd) + " \n"
    
    if listSellBuy is not None:
        countSellBuy = len(listSellBuy)
        usedCoin = sum([listSellBuy[x]["Quantity"] for x in listSellBuy])
        totalFiatSell = sum( [listSellBuy[x]["SellValue"] * listSellBuy[x]["Quantity"] for x in listSellBuy])
        print(totalFiatSell)
        totalFiatBuy =  usedCoin*pricenow
        lose = totalFiatSell -totalFiatBuy
        string_text = string_text + "List Buy Sell : "+ str(countSellBuy) + " Trade use " +  str(round(usedCoin,4)) + " "+ str(Coin) +"\n"
        string_text =  string_text + "If buy all now, we will lose :  " + str(round(lose,3)) +" "+ str(Usd) + " \n"

    update.message.reply_text(string_text)
  
def TotalProfit(update: Update, context: CallbackContext):
    stringtext= ""
    profit = CalProfit.ProfitAll()
    listProfit =profit[0]
    totalprofit =profit[1]
    print(listProfit, totalprofit)
    for x,y in listProfit:
        stringtext =stringtext + "Day " + str(x) + " : " + str(round(y,2)) + " USD \n"
    
    stringtext = stringtext + "\nTotal Profit All Day: " + str(round(totalprofit,3)) + " USD \n"
    update.message.reply_text(stringtext)
  
  
def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry '%s' is not a valid command" % update.message.text)

  
  
def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry I can't recognize you , you said '%s'" % update.message.text)
  
 
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('balance', balance))
updater.dispatcher.add_handler(CommandHandler('TotalProfit', TotalProfit))
updater.dispatcher.add_handler(CommandHandler('Info_trading', Info_trading))
#updater.dispatcher.add_handler(CommandHandler('Delete_Trade_Done', Firebase.Auto_delete_TradeDone()))

updater.dispatcher.add_handler(MessageHandler(Filters.text('start'),start))
updater.dispatcher.add_handler(MessageHandler(Filters.text('help'),help))
updater.dispatcher.add_handler(MessageHandler(Filters.text('balance'),balance))
updater.dispatcher.add_handler(MessageHandler(Filters.text('profit'),TotalProfit))
updater.dispatcher.add_handler(MessageHandler(Filters.text('info trading'),Info_trading))
#updater.dispatcher.add_handler(MessageHandler(Filters.text('Update_Delete_trading'),Firebase.Auto_delete_TradeDone()))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))


updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown))  # Filters out unknown commands
  
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))


updater.start_polling()





#https://pretagteam.com/question/telegram-bot-send-message-every-hour-python


""" from telegram.ext import Updater, InlineQueryHandler, CommandHandler



TOKEN= '5020937139:AAGfNblKv-ohgSZCabNrLmNNvopZ_Bpl7qA'

def start(update,context):
    update.message.reply_text("Hello! Welcome to bot trading of Tamhv")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start"))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main() """

