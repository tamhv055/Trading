class coupleSellBuy:
    def __init__(self,buyprice,sellprice,done):
        self.buy  = buyprice
        self.sell = sellprice
        self.done = False
    

    def getDistSB(seft):
        return {'buy':seft.buy,'sell':seft.sell}

    def sellpricefuture(self):
        return float(self.buy*float(1+0.005))

    def buypricefuture(self):
        return float(self.sell*float(1-0.005))