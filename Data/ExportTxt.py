import time


timestr = time.strftime("%d-%m-%Y----%H-%M-%S")
print(timestr)





def writeDataNow(data):
    timestr = time.strftime("%d-%m-%Y")
    with open('D:\project Binance\Data\DataBackup'+'\\'+timestr+'.txt','w') as f:
        f.write(str(data))



# datatrade = [[1,2],[3,4],[2,5],[6,9],[1,7],[5,3]]
# writeDataNow(datatrade)