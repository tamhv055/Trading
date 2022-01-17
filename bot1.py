from asyncio import sleep
import sys
import threading

sys.path.insert(1, "D:\project Binance")  
sys.path.insert(1, "D:\project Binance\Data")  
sys.path.insert(1, "D:\project Binance\BinanceApi")
sys.path.insert(1, "D:\project Binance\Logic")
sys.path.insert(1, "D:\project Binance\LogFile")
sys.path.insert(1, "D:\project Binance\Bot_telegram")

from binance.client import Client, BaseClient
from binance.enums import *
from binance.exceptions import BinanceAPIException
import json
import time
from Data import GetData
from Data import Firebase
from BinanceApi import BinanceTrading
from Logic import Trading
import config

import os
from pynput import keyboard
import time

import logging
import logging.handlers as handlers
from threading import Timer
from threading import Thread


logger = logging.getLogger()
logger.setLevel(logging.INFO)

## Here we define our formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logHandler = handlers.TimedRotatingFileHandler('/project Binance/LogFile/info_trading.log', when="midnight", interval=1, backupCount=0)
logHandler.suffix='%d-%m-%Y.log'
logHandler.setLevel(logging.INFO)
logHandler.setFormatter(formatter)


errorLogHandler = handlers.RotatingFileHandler('/project Binance/LogFile/error.log' , maxBytes=5000, backupCount=0)
errorLogHandler.setLevel(logging.ERROR)
errorLogHandler.setFormatter(formatter)


logger.addHandler(logHandler)
logger.addHandler(errorLogHandler)


def autoUpdateFirebase():
    while True:
        logging.info("auto Update Delete Firebase")
        Firebase.Auto_delete_TradeDone()
        time.sleep(86400)
    



try:
    threading.Thread(target=autoUpdateFirebase).start()
    threading.Thread(target=Trading.TradeAllTime).start()
    
    
except Exception as e:
    logger.error("Bot1 error code 58:"+str(e))
    """ Bot_telegram.updater.bot.send_message(chat_id = UserId,text = "Bot1 error code 62: ")
    Bot_telegram.updater.bot.send_message(chat_id = UserId,text = str(e)[:400]) """
    #Bot.send_message(chat_id = UserId,text = "Bot1 error code 62: ")
    #Bot.send_message(chat_id = UserId,text = str(e)[:400])
else:
    logger.info("Restart run TradeAllTime")


#Bot_Trading.TradeAllTime()

""" while 1:
    os.system("python 'd:/project Binance/bot1.py'")
    exit() """

#timestr = time.strftime("%d-%m-%Y----%H-%M-%S")33333333333333333333




#https://www.geeksforgeeks.org/python-script-to-monitor-network-connection-and-saving-into-log-file/