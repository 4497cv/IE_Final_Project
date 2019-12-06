import sys
try:
    from Tkinter import *
except:
    from tkinter import *

from serial import Serial

def serial_port():
    try:
        port = Serial('/dev/ttyUSB0', 115200, timeout=0)
    except:
        print("tty USB0 not available")

    while 1:
        port.flush()
        data = port.readline()
        print(data)



def main():
    try:
        port = Serial('/dev/ttyUSB0', 115200, timeout=0)
    except:
        print("tty USB0 not available")

    
    root = Tk()
    menu = Menu(root)
    root.config(menu=menu)
    filemenu = Menu(menu)
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=RIGHT, fill=Y)
    mylist = Listbox(root, yscrollcommand = scrollbar.set)

    port.flush()

    port.flush()
    data = str(port.readline())
    mylist.insert(END, data)

    port.flush()
    data = str(port.readline())
    mylist.insert(END, data)

    mylist.pack(side=LEFT, fill=BOTH)
    scrollbar.config(command =mylist.yview)
    mainloop() # open window   






main()
