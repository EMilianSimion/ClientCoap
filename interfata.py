"""Un pic de interfata"""
import tkinter as tk
from format import Header
from message import Pack
from client import *

from tkinter import ttk
h=""
p=0
r=""
m=""
c=0
consola = "emi"

class HelloView(tk.Frame):
    """A friendly little module"""
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)


        self.host = tk.StringVar()
        self.port = tk.IntVar()
        self.resource = tk.StringVar()
        self.request = tk.StringVar()
        self.out = tk.StringVar()
        self.confirmable = tk.IntVar()
        self.post = tk.StringVar(value = "Iasi")


        self.host.set("127.0.0.1")
        self.port.set(5006)
        self.resource.set("score")
        self.request.set("get")
        self.out.set("-----------------------------12/09/2019-------------------------------")

        combo_resource = ttk.Combobox(self, values=["SCORE", "RedCards", "YellowCars", "Corners", "Offsides"], textvariable=self.resource)
        combo_request = ttk.Combobox(self, values=["Get", "POST", "CUSTOM"], textvariable=self.request)
        spinbox_port = ttk.Spinbox(self, from_=0.0, to=10000, increment=1, textvariable=self.port)

        combo_resource.current(0)
        combo_request.current(0)

        host_label = ttk.Label(self, text="Host")
        port_label = ttk.Label(self, text="Port")
        resource_label = ttk.Label(self, text="Resource")
        request_label = ttk.Label(self,text="Request Method")
        confirmable_label = ttk.Label(self, text="Confirmable")
        output_label = ttk.Label(self, textvariable=self.out, wraplength=600)
        post_label = ttk.Label(self, text ="Post")


        host_entry = ttk.Entry(self, textvariable=self.host)
        post_entry = ttk.Entry(self, textvariable = self.post)
        #port_entry = ttk.Entry(self, textvariable=self.port)
        #resource_entry = ttk.Entry(self, textvariable=self.resource)
        #request_entry = ttk.Entry(self, textvariable=self.request)

        run_button = ttk.Button(self, text="Run", command=self.on_change)
        confirmable_button = ttk.Checkbutton(confirmable_label, text="Confirmable", variable=self.confirmable)

        host_label.grid(row=0, column=0, sticky=tk.W)
        host_entry.grid(row=0, column=1, sticky=(tk.N+tk.W))
        port_label.grid(row=1, column=0,sticky=tk.W)
        spinbox_port.grid(row=1, column=1, sticky=(tk.N+tk.W))
        resource_label.grid(row=2, column=0, sticky=tk.W)
        combo_resource.grid(row=2, column=1, sticky=(tk.N+tk.W))
        request_label.grid(row=3, column=0, sticky=tk.W)
        combo_request.grid(row=3, column=1, sticky=(tk.N+tk.W))
        post_label.grid(row=4, column=0, sticky=tk.W)
        post_entry.grid(row=4, column=1, sticky=(tk.N + tk.W))
        confirmable_label.grid(row=5, column=0,sticky=tk.W)
        confirmable_button.grid(row=5,column=0, sticky=tk.W)
        run_button.grid(row=6,column=2,sticky=tk.N)
        output_label.grid(row=7, column=0, columnspan=3)


    def on_change(self):
        global h, p, r, m, c

        if self.host!="" and self.port!="" and self.resource!="" and self.request!="":
            # self.out.set(" Host "+self.host.get()+"\n Port "+str(self.port.get())+"\n Resource "+self.resource.get()
            #               +"\n Request Method "+self.request.get()+ "\n Confirmable " +str(self.confirmable.get()))
            h,p,r,m,c = self.take_data()
            self.out.set(consola)
        else:
            self.out.set("\n----------------Emi------------")
    def take_data(self):
        return self.host.get(), self.port.get(), self.resource.get(), self.request.get(), self.confirmable.get()

class MyApplication(tk.Tk):
    """Hello World Main Application"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Client-Server")
        self.geometry("800x600")

        self.text = ""

        self.resizable(width=False, height=False)

        HelloView(self).grid(sticky=(tk.E + tk.W + tk.N + tk.S))
        self.columnconfigure(0, weight=1)
    def take_data(self):
        return h, p, r, m, c
    def update(self, text):
        global consola
        self.text += text
        consola = text

