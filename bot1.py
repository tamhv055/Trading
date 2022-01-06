import sys
sys.path.insert(1, "D:\project Binance")  
sys.path.insert(1, "D:\project Binance\Data")  
sys.path.insert(1, "D:\project Binance\BinanceApi")
sys.path.insert(1, "D:\project Binance\Logic")
sys.path.insert(1, "D:\project Binance\LogFile")

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
from LogFile import Writelog
from pynput import keyboard
import time








Trading.TradeAllTime()
#Bot_Trading.TradeAllTime()

""" while 1:
    os.system("python 'd:/project Binance/bot1.py'")
    exit() """

#timestr = time.strftime("%d-%m-%Y----%H-%M-%S")33333333333333333333




#https://www.geeksforgeeks.org/python-script-to-monitor-network-connection-and-saving-into-log-file/