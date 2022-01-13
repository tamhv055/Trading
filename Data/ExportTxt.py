import time
import sys 
import logging



def writeDataNow(data):
    timestr = time.strftime("%d-%m-%Y")
    with open('D:\project Binance\LogFile\DataBackup'+'\\'+timestr+'.txt','w') as f:
        f.write(str(data))





# datatrade = [[1,2],[3,4],[2,5],[6,9],[1,7],[5,3]]
# writeDataNow(datatrade)