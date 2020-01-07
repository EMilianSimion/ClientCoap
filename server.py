import socket
from _thread import *
import threading
from format import Header
from message import Pack

UDP_IP = '127.0.0.1'
UDP_PORT = 5006
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

#lock = threading.Lock()
headerRecv = Header()
headerSend = Header()
packRecv = Pack()
packSend = Pack()
headerSend.setHeader1(1,1,4)
headerSend.setCode(0,1)
headerSend.setMessageId(29)
headerSend.setToken(68)
headerSend.buildHeader()

dataSent=""

print("-------------------------------------Wait connections-----------------------------------------")
while 1:
    data, addr = sock.recvfrom(1024)
    #lock.acquire()
    #start_new_thread(process, (addr, data,))
    if not data:
        break
    packRecv.set(data)
    head, mesg = packRecv.dispackPack()
    headerRecv.setHeader(head)
    headerRecv.buildHeader()
    headerRecv.setCode(headerRecv.getCodeClass(), headerRecv.getCodeDetail())
    if headerRecv.getCode() !=0:

        print("received",len(data), "bytes from ", addr)
        print("data de la client ", mesg )
        if mesg == "Score":
            dataSent = "2-0"
        if mesg == "Red":
            dataSent = "3REdCards"
        if mesg == "Yellow":
            dataSent = "8Yellow Cards"

        packSend.buildPack(headerSend, dataSent)
        sock.sendto(packSend.getPackege(), addr)
        #sock.sendto(packSend.getPackege(), addr)
    else:
        print("ACK recive")

#sock.close()