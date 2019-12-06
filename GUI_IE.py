
import sys
import time

try:
    import Tkinter as tk
except:
    import tkinter as tk 

try:
    from serial import Serial
except:
    print("could not import serial module")


#GUI Functions
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

class THDS(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.wm_title("THDS")
        self.geometry('350x280')
        self.configure(background='white')

        selfWidth = self.winfo_reqwidth() 	#get self width
        selfHeight = self.winfo_reqheight()	#get self height

        positionX = int((self.winfo_screenwidth()/2)-(selfWidth))
        positionY = int((self.winfo_screenheight()/2)-(selfHeight))

        self.geometry("+{}+{}".format(positionX, positionY))
        self.resizable(False, False)

        lbl_empty = tk.Label(self, text = "        ", bg="white", width = 17, height=2)
        lbl_empty.grid(column = 3, row = 0)
        lbl_title = tk.Label(self, text = "   Temperature, Humidity, and Gas Detection System   ", bg="white", font="Times")
        lbl_title.grid(column = 3, row = 1)
        
        lbl_empty = tk.Label(self, text = "		", bg="white", width = 17, height=2)
        lbl_empty.grid(column = 3, row = 2)
    
        btn1 = tk.Button(self, text = "Temperature Sensor", width = 17, height=1, font="Times",borderwidth=3)
        btn1.grid(column = 3, row = 5)
        lbl_empty = tk.Label(self, text = "		", bg="white")
        lbl_empty.grid(column = 3, row = 6)
        btn2 = tk.Button(self, text = "Humidity Sensor", width = 17, height=1, font="Times",borderwidth=3)
        btn2.grid(column = 3, row = 7)
        lbl_empty = tk.Label(self, text = "		", bg="white")
        lbl_empty.grid(column = 3, row = 8)
        btn2 = tk.Button(self, text = "Gas Sensor", width = 17, height=1, font="Times",borderwidth=3)
        btn2.grid(column = 3, row = 9)
        self.mainloop()
        
    def _quit(self):
        self.quit()
        self.destroy()        

    # menu = Menu(root)
    # root.config(menu=menu)
    # filemenu = Menu(menu)
    # scrollbar = Scrollbar(root)
    # scrollbar.pack(side=RIGHT, fill=Y)
    # mylist = Listbox(root, yscrollcommand = scrollbar.set)

    # port.flush()

    # port.flush()
    # data = str(port.readline())
    # mylist.insert(END, data)

    # port.flush()
    # data = str(port.readline())
    # mylist.insert(END, data)

    # mylist.pack(side=LEFT, fill=BOTH)
    # scrollbar.config(command =mylist.yview)
    # mainloop() # open window   

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
     

#main()
#GUI_main_menu()

app = THDS();
app.GUI_Quit();