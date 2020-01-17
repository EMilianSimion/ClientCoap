def enum(**enums):
    return type('Enum', (), enums)

def CoapResponseCode(class_, detail):
    """ """
    return ((class_ << 5) | (detail))

COAP_TYPE = enum(
    COAP_CON=1,
    COAP_NONCON=0,
    COAP_ACK=2,
    COAP_RESET=3
)
COAP_METHOD = enum(
    COAP_EMPTY = 0,
    COAP_GET=1,
    COAP_POST=2,
    COAP_PUT=3,
    COAP_DELETE=4,
    COAP_CUSTOM =5
)
COAP_RESPONSE_CODE = enum(
    COAP_CREATED=[2,1],
    COAP_DELETED=[2, 2],
    COAP_VALID=[2, 3],
    COAP_CHANGED=[2, 4],
    COAP_CONTENT=[2, 5],
    COAP_BAD_REQUEST=[4, 0],
    COAP_UNAUTHORIZED=[4, 1],
    COAP_BAD_OPTION=[4, 2],
    COAP_FORBIDDEN=[4, 3],
    COAP_NOT_FOUND=[4, 4],
    COAP_METHOD_NOT_ALLOWD=[4, 5],
    COAP_NOT_ACCEPTABLE=[4, 6],
    COAP_PRECONDITION_FAILED=[4, 12],
    COAP_REQUEST_ENTITY_TOO_LARGE=[4, 13],
    COAP_UNSUPPORTED_CONTENT_FORMAT=[4, 15],
    COAP_INTERNAL_SERVER_ERROR=[5, 0],
    COAP_NOT_IMPLEMENTED=[5, 1],
    COAP_BAD_GATEWAY=[5, 2],
    COAP_SERVICE_UNAVALIABLE=[5, 3],
    COAP_GATEWAY_TIMEOUT=[5, 4],
    #COAP_PROXYING_NOT_SUPPORTED=CoapResponseCode(5, 5)
)

class Header:
    def __init__(self):
        self.header=None

        #ver t tkl
        self.header1=None
        #code format
        self.code=None

        self.version = 0
        self.messageType = 0
        self.tokenLength = 0
        self.codeClass = 0
        self.codeDetail = 0
        self.messageId = 0
        self.token = 0

    def setHeader(self,msg):
        self.header=msg
        self.version=self.header[0:2]
        self.messageType = self.header[2:4]
        self.tokenLength = self.header[4:8]
        self.codeClass = self.header[8:11]
        self.codeDetail= self.header[11:16]
        self.messageId = self.header[16:32]
        if(self.getTokenLength()>0):
            self.token = self.header[32:32+self.getTokenLength()*8]
        else:
            self.token=None
    def setMessageId(self,a):
        self.messageId=format(a,'016b')

    def setToken(self,a):
        if(self.getTokenLength()>0 and self.getTokenLength()<8):
            self.token=format(a,'0'+str(self.getTokenLength()*8)+'b')

    def setHeader1(self,version,type,tkl):
        self.version=format(version,'02b')
        self.messageType = format(type,'02b')
        self.tokenLength=format(tkl,'04b')
        self.header1=(version<<6)+(type<<4)+tkl
        self.header1=format(self.header1,'08b')

    def setCode(self, clas, detail):
        self.codeClass = format(clas, '03b')
        self.codeDetail = format(detail, '05b')
        self.code = (clas << 5)+detail
        self.code = format(self.code, '08b')

    def buildHeader(self):
        if(self.getTokenLength()>0):
            self.header=""+str(self.header1)+str(self.code)+str(self.messageId)+str(self.token)
        else:
            self.header=""+str(self.header1)+str(self.code)+str(self.messageId)
        return self.header

    def getTokenLength(self):
        return int(str(self.tokenLength),2)

    def getVersion(self):
        return int(str(self.version),2)

    def getMessageType(self):
        return int(str(self.messageType),2)

    def getCodeClass(self):
        return int(str(self.codeClass),2)

    def getCodeDetail(self):
        return int(str(self.codeDetail),2)

    def getCode(self):
        return int(str(self.code),2)

    def getMessageId(self):
        return int(str(self.messageId),2)

    def getToken(self):
        return int(str(self.token),2)


    def nextMessageId(self):
        """Reserve and return a new messageId"""
        message_id=self.messageId
        self.messageId=0xFFFF&(1+self.messageId)
        return message_id
    def nextToken(self):
        """Reserve and return a new Token for request"""
        token=self.token
        self.token=(self.token+1)&0xffffffffffffffff
        return token

    def print(self):
        print("\n\nHeaderul-> ")
        print("Version= " + str(self.getVersion()))
        print("Message Type= " + str(self.getMessageType()))
        print("Token Length=" + str(self.getTokenLength()))
        print("CodeClass= " + str(self.getCodeClass()))
        print("CodeDetail= " + str(self.getCodeDetail()))
        print("MessageId=" + str(self.getMessageId()))
        print("Token=", str(self.getToken()))
        print("Headerul-> " + str(self.header))
        print("Header size->" + str(len(self.header)))
