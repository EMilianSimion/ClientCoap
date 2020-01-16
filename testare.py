from format import Header
from message import Pack
from client import *

ip = '127.0.0.1'
port = 5006
version = 2
tkl = 4

# header=Header()
# header.setHeader1(1,2,4)
# header.setCode(0,1)
# header.setMessageId(29)
# header.setToken(68)
# header.buildHeader()
#
# header.print()
#package = Pack()
#package.buildPack(header,"Score")
#print(package.getPackege())

##############################################3

coap = Caop()
coap.start()
print("Mesajul trimis de client Score")
coap.get(ip, port, 'Score', COAP_TYPE.COAP_NONCON)
print("Mesajul trimis de client Red")
coap.get(ip, port, 'RedCards', COAP_TYPE.COAP_NONCON)
print("Mesajul trimis de client Yellow")
coap.get(ip, port, 'YellowCars', COAP_TYPE.COAP_NONCON)
###############################################
# #
# header = Header()
# header.setHeader1(1,2,0)
# header.setCode(0,1)
# header.setMessageId(29)
# header.setToken(68)
# header.buildHeader()
# # header.print()
#
# # package = Pack()
# # # # package.buildPack(header,"Score")
# # # pack = ("" + str(header.header) + "Score").encode()
# # #
# # # print(pack)
# # # print(pack.decode())
# # package.buildPack(header, "Maria Ioana")
# # print(package.getPackege())
# # print(package.dispackPack())
# print(header.getCode())