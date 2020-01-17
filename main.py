from format import Header
from message import Pack
from client import *
from interfata import MyApplication
from thClient import Client

ip = '127.0.0.1'

port = 5006
version = 2
tkl = 4

text =""
app = MyApplication()
coap = Caop()
coap.start()


def task():
    app.after(2000, task)
    (h, p, r, m, c) = app.take_data()
    print("cererea citita de pe interfata", r)
    run(h, p, r, m, c)
    app.update(text)
def run(my_host, my_port, my_cerere, my_metoda, my_type):
    global text
    if not my_cerere:
        coap.get(ip, port, "Score", COAP_TYPE.COAP_NONCON)
    else:
        if my_metoda =="Get":
            coap.get(my_host, my_port, str(my_cerere), my_type)#str(cerere)
        elif my_metoda =="POST":
            coap.post(my_host, my_port, str(my_cerere), my_type)
        elif my_metoda == "CUSTOM":
            coap.custom(my_host, my_port, str(my_cerere), my_type)

    text = coap.getResult()
if __name__ == '__main__':
    app.after(2000, task)
    app.mainloop()


