from client import Caop
import threading
class Client(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.coap = Caop()
        self.coap.start()
        self.ip = '127.0.0.1'
        self.port = 5006
        self.message = ""

    def run(self):
        self.coap.get(self.ip, self.port, 'Score')
        self.message = self.coap.getResult()

    def returnMessage(self):
        return self.message