class Message:
    def __init__(self):
        self.format=""
        self.message=""
        self.package=""

    def buildMessage(self,format,message):
        self.format=format
        self.message=message
        if(message==""):
            self.package=self.format.encode()
        else:
            self.package=(""+str(self.format)+str(self.message)).encode()
        return self.package
    def dispackMessage(self):
        dispack=self.package.decode()
        tokenLength=int(str(dispack[4:8]),2)
        self.format=dispack[0:32+tokenLength*8]
        self.message=dispack[32+tokenLength*8:]
        return(self.format,self.message)

    def getPackege(self):
        return self.package

