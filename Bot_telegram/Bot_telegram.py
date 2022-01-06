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
from Data import GetData
from config import Coin, Usd 

updater = Updater("5020937139:AAGfNblKv-ohgSZCabNrLmNNvopZ_Bpl7qA",
                  use_context=True)
  
  
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Hello sir, Welcome to the Bot.Please write\
        /help to see the commands available.")
  
def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :-
    /youtube - To get the youtube URL
    /balance - To get blance
    /totalprofit - To get all profit""")
  
  
def balance(update: Update, context: CallbackContext):
    BalanceCoin = GetData.get_balance_Coin_Free(Coin)
    BalanceUSD = GetData.get_balance_USDT_Free(Usd)
    reply_text = "Balance of "+ str(Coin) + ": " + str(BalanceCoin)
    reply_text =reply_text+ "\nBalance of " + str(Usd) + ": " + str(BalanceUSD)
    
    update.message.reply_text(reply_text)
  
  
  
  
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
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown))  # Filters out unknown commands
  
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))
  
updater.start_polling()






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

