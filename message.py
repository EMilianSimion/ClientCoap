class Pack:
    def __init__(self):
        self.header = ""
        self.message = ""
        self.package = ""

    def set(self, pack):
        self.package = pack

    def buildPack(self,header,message):
        self.header = header
        self.message = message
        if(message == ""):
            self.package=("" + str(self.header)).encode()
        else:
            self.package = (""+str(self.header.header)+str(self.message)).encode()
        return self.package
    def dispackPack(self):
        dispack=self.package.decode()
        # tokenLength=int(str(dispack[4:8]),2)
        tokenLength = 4
        self.header=dispack[0:32+tokenLength*8]
        self.message=dispack[32+tokenLength*8:]
        return(self.header,self.message)

    def getPackege(self):
        return self.package

