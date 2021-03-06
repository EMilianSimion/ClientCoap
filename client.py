import socket
import select
from format import *
from message import Pack
from random import randint
import threading

_COAP_DEFAULT_PORT = 5006
_COAP_DEFAULT_VERSION = 2
_COAP_DEFAULT_TKL = 4
_COAP_BUF_MAX_SIZE = 1024

_COAP_DEFAULT_AKC_TIMEOUT = 2
_COAP_DEFAULT_AKC_RANDOM_FACTOR = 1.5
_COAP_DEFAULT_MAX_RETRANSMIT = 5
_COAP_DEFAULT_TIMEOUT = 2


class Caop:
    def __init__(self):
        self.sock = None
        self.callbacks = {}
        self.responseCallback = None
        self.port = 0
        self.result = ""

    def start(self, addr='127.0.0.1', port=_COAP_DEFAULT_PORT):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # self.sock.bind((addr, port))

    def stop(self):
        if self.sock is not None:
            self.sock.close()
            self.sock = None

    def sendPacket(self, ip, port, header, messaj):
        coapPacket = Pack()
        coapPacket.buildPack(header, messaj)
        status = 0
        try:
            sockaddr = (ip, port)
            status = self.sock.sendto(coapPacket.getPackege(), sockaddr)
            if (status > 0):
                status = header.getMessageId()
            # print('Packet sent. MessageId', status)
        except Exception as e:
            status = 0
            print('Exception while sending packet...')
        return status

    def send(self, ip, port, version, type, tkl, method, token, payload):
        header = Header()
        header.setHeader1(version, type, tkl)
        token = randint(0, 65536)
        header.setToken(token)
        header.setCode(0, method)

        return self.sendEx(ip, port, header, payload)

    def sendEx(self, ip, port, header, payload):
        nextMessage = randint(0, 65536)
        header.setMessageId(nextMessage)
        header.buildHeader()
        return self.loop(ip, port, header, payload, _COAP_DEFAULT_MAX_RETRANSMIT)

    def sendResponse(self, ip, port, version, tkl, messageid, payload, code, token):
        header = Header()
        header.setHeader1(version, COAP_TYPE.COAP_ACK, tkl)
        header.setCode(code[0], code[1])
        header.setMessageId(messageid)
        header.setToken(token)
        header.buildHeader()

        return self.sendPacket(ip, port, header, payload)

    def readBytesFromSocket(self, numOfBytes):
        try:
            return self.sock.recvfrom(numOfBytes)
        except Exception:
            return None, None

    def get(self, ip, port, url, type):
        return threading.Thread(target = self.send(ip, port, _COAP_DEFAULT_VERSION, type, 4, COAP_METHOD.COAP_GET, 0, url)).start()
    def post(self, ip, port, url,type ):
        return threading.Thread(target = self.send(ip, port, _COAP_DEFAULT_VERSION,type, 4, COAP_METHOD.COAP_POST, 0, url )).start()
    def custom(self, ip, port, url, type):
        return threading.Thread(target = self.send(ip, port, _COAP_DEFAULT_VERSION, type, 4, COAP_METHOD.COAP_CUSTOM, 0, url)).start()

    def handleIncommingResponse(self, header, message):

        #header.print()
        self.result ="Mesajul este "+ str(message)
        print("Mesajul receptionat de la server "+ str(message))
    def getResult(self):
        return self.result

    def sendACK(self, ip, port, messID, token):
        header = Header()
        header.setHeader1(_COAP_DEFAULT_VERSION, COAP_TYPE.COAP_ACK, _COAP_DEFAULT_TKL)
        header.setCode(0, 0)
        header.setMessageId(messID)
        header.setToken(token)
        header.buildHeader()
        self.sendPacket(ip, port, header, "")

    def codeGet(self,header):
        if header.getCodeClass() ==2 and header.getCodeDetail() ==3:
            print("COAP_VALID")
            return 1
        elif header.getCodeClass() ==2 and header.getCodeDetail() ==5:
            print("COAP_CONTENT")
            return 1
        elif header.getCodeClass() ==4 and header.getCodeDetail() ==5:
            print ("COAP_METHOD_NOT_ALLOWD")
        return 0

    def codeput(self, header):
        if header.getCodeClass() == 2 and header.getCodeDetail() == 1:
            print("COAP_CREATED")
            return 1
        if header.getCodeClass() == 2 and header.getCodeDetail() == 4:
            print("COAP_CHANGED")
            return 1
        if header.getCodeClass() == 4 and header.getCodeDetail() == 5:
            print("COAP_METHOD_NOT_ALLOWD")
        return 0

    def verifyCodeRcv(self, headerSent, headerRecv):
        if headerSent.getCode() == COAP_METHOD.COAP_GET :
            return self.codeGet(headerRecv)
        elif headerSent.getCode() == COAP_METHOD.COAP_POST:
            return self.codeput(headerSent)


    def loop(self, ip, port, header, message, retransmit):
        global headerRcv
        if header.getMessageType() == COAP_TYPE.COAP_CON:
            # CON
            print("Trimit CON")
            self.sendPacket(ip, port, header, message)

            # self.sock.settimeout(_COAP_DEFAULT_AKC_TIMEOUT)
            r, _, _ = select.select([self.sock], [], [], _COAP_DEFAULT_AKC_TIMEOUT)
            # WaitForACK
            if not r:
                print("Nu s a receptionat un raspuns de la server, Adica un ACK")
                print("Trimit din nou CON")
                retransmit = retransmit - 1
                # WaitForExpirationMID
                if retransmit != 0:
                    self.loop(ip, port, header, message, retransmit)
                else:
                    print("Am trimis de " + str(_COAP_DEFAULT_MAX_RETRANSMIT) + " ori. Nu am primit nici un raspuns")

            else:
                # Recieve ACK
                headerRcv = Header()
                buffer = Pack()

                (data, remoteAddress) = self.readBytesFromSocket(_COAP_BUF_MAX_SIZE)
                buffer.set(data)
                (head, message) = buffer.dispackPack()
                headerRcv.setHeader(head)
                headerRcv.buildHeader()
                headerRcv.setCode(headerRcv.getCodeClass(), headerRcv.getCodeDetail())
            # piggy-backed?
            # print("--------------piggy-backed---------------getCode--------------" + str(headerRcv.getCode()))

            if headerRcv.getCode() != 0:   #header.getCode() == Content
                # piggybacked
                if self.verifyCodeRcv(header, headerRcv) ==0:
                    print("aici iesi")
                    return

                # -----------------------------?
                #if headerRcv.getMessageId() == header.getMessageId()  and headerRcv.getToken() == header.getToken():
                return self.handleIncommingResponse(headerRcv, message)
                # else:
                #     print("Piggy-backed not match")
            else:
                # No piggybacked
                ######
                r, _, _ = select.select([self.sock], [], [], _COAP_DEFAULT_TIMEOUT)
                if not r:
                    print("Nu s a receptionat un raspuns ")
                else:
                    print("empty message recv. Message sent has token :" + str(header.getToken()) )
                    headerRcv = Header()
                    pack = Pack()
                    (buffer, remoteAddress) = self.readBytesFromSocket(_COAP_BUF_MAX_SIZE)
                    pack.set(buffer)
                    (head, message) = pack.dispackPack()
                    headerRcv.setHeader(head)
                    headerRcv.buildHeader()
                    # RespType?
                    # RespCON
                    print("-----------------------------" +str(headerRcv.getMessageType()))
                    if headerRcv.getMessageType() == COAP_TYPE.COAP_CON:
                        # trasnmitACK
                        print("----------------------------------Sent ACK")
                        print("---------------------------------" + str(headerRcv.getMessageId()))
                        self.sendACK(ip, port, headerRcv.getMessageId(), headerRcv.getToken())
                    # ReturnResponse
                    # ------------------------?
                    # if headerRcv.getToken() == header.getToken():
                    return self.handleIncommingResponse(headerRcv, message)
                    # else:
                    #     print("Separate response not match")
                #######
        else:       
            # NON
            print("Trimit NONCON")
            self.sendPacket(ip, port, header, message)
            # self.sock.settimeout(_COAP)
            # WaitForResp
            r, _, _ = select.select([self.sock], [], [], _COAP_DEFAULT_TIMEOUT)
            if not r:
                print("Nu s a receptionat un raspuns ")
            else:
                headerRcv = Header()
                pack = Pack()
                (buffer, remoteAddress) = self.readBytesFromSocket(_COAP_BUF_MAX_SIZE)
                pack.set(buffer)
                (head, message) = pack.dispackPack()
                headerRcv.setHeader(head)
                headerRcv.buildHeader()
                # RespType?
                # RespCON
                if self.verifyCodeRcv(header, headerRcv) ==0:
                    print("aici iesi")
                    return
                if headerRcv.getMessageType() == COAP_TYPE.COAP_CON:
                    # trasnmitACK
                    self.sendACK(ip, port, headerRcv.getMessageId(), headerRcv.getToken())
                    print("---------------------->", str(headerRcv.getMessageId()) + str(headerRcv.getToken()))
                # ReturnResponse
                # --------------------?
                # if headerRcv.getToken() == header.getToken():
                return self.handleIncommingResponse(headerRcv, message)
                # else:
                #     print("Nonconf message not match")

