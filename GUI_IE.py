
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
def serial_port_init():
    serial_port_id = '/dev/ttyUSB0'
    global port 

    try:
        port = Serial(serial_port_id, 115200, timeout=0)
        print("conncted to " + serial_port_id + "\n\r")
        app = THDS();
    except:
        print("serial port "+ serial_port_id + " is not available\n\r")
        print("closing program..\n\r")

def serial_port_readline(): 
    while 1:
        port.flush()
        data = port.readline()
        print(data)

def main():
    serial_port_init()

def serial_temperature_request():
    print("requesting temperature to the atmega..\n\r")
    
    data = 'REQ_'

    #Waiting for request confirmation
    while data != 'REQ_TEMP_OK':
        port.flush()
        time.sleep(1)
        port.write('1')
        time.sleep(1)
        port.flush()
        data = port.readline()
        print(data)

    print("Temperature reading request OK\n\r")



##EVENT HANDLERS       
def temperature_button_event_handler():
    print("temperature button pressed\n\r")
    serial_temperature_request()
    serial_port_readline()

def humidity_button_event_handler():
    print("humidity button pressed\n\r")

def gas_button_event_handler():
    print("gas button pressed\n\r")

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
    
        btn1 = tk.Button(self, text = "Temperature Sensor", width = 17, height=1, font="Times",borderwidth=3, command=temperature_button_event_handler)
        btn1.grid(column = 3, row = 5)
        lbl_empty = tk.Label(self, text = "		", bg="white")
        lbl_empty.grid(column = 3, row = 6)
        btn2 = tk.Button(self, text = "Humidity Sensor", width = 17, height=1, font="Times",borderwidth=3, command=humidity_button_event_handler)
        btn2.grid(column = 3, row = 7)
        lbl_empty = tk.Label(self, text = "		", bg="white")
        lbl_empty.grid(column = 3, row = 8)
        btn2 = tk.Button(self, text = "Gas Sensor", width = 17, height=1, font="Times",borderwidth=3, command=gas_button_event_handler)
        btn2.grid(column = 3, row = 9)
        self.mainloop()
        
    def _quit(self):
        self.quit()
        self.destroy()        

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
     

#main()
#GUI_main_menu()


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
main()