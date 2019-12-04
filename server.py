import socket
from _thread import *
import threading
from format import Format
from message import Message

UDP_IP = '127.0.0.1'
UDP_PORT = 80
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((UDP_IP, UDP_PORT))

#lock = threading.Lock()

print("-------------------------------------Wait connections-----------------------------------------")
#while 1:
    #data, addr = s.recvfrom(1024)
    #lock.acquire()
    #start_new_thread(process, (addr, data,))
s.close()