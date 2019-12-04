import socket
from format import Format
from message import Message

UDP_IP = '127.0.0.1'
UDP_PORT = 80
s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.connect((UDP_IP,UDP_PORT))


header=Format()
header.setHeader1(1,2,4)
header.setCode(0,1)
header.setMessageId(29)
header.setToken(68)
header.buildFormat()

package=Message()
package.buildMessage(header.format,"score")
print("--------------------------------------------------sending----------------------------------------------------")
s.sendto(package.getPackege(),(UDP_IP,UDP_PORT))
data=s.recvfrom(1024)
print(data[0].decode())
print(header.format)

s.close()