####################################################################################
#  \file:   GUI_IE.py                                                              #
#  \brief:  This file contains the graphical user interface for THGDS              #
#  \author: Cesar Villarreal @4497cv                                               #
#  \date:   04/12/2019                                                             #
####################################################################################

import sys
import time

try:
    import Tkinter as tk
    from Tkinter import Menu
except:
    import tkinter as tk 
    from tkinter import Menu

try:
    from serial import Serial
except:
    print("could not import serial module")

#                               GUI Functions

##################################################################################
#  \brief:      This function intializes the serial port communication           #
#  \param[in]:                                                                   #
#  \param[out]:                                                                  #
##################################################################################
def serial_port_init():
    serial_port_id = '/dev/ttyUSB0'
    global port 

    try:
        port = Serial(serial_port_id, 115200, timeout=0)
        print("conncted to " + serial_port_id + "\n\r")
        app = THDS();
        ver = True
    except:
        print("serial port "+ serial_port_id + " is not available\n\r")
        print("closing program..\n\r")
        ver = False
    
    return ver



##################################################################################
#  \brief:      This function reads data from the serial port                    #
#  \param[in]:                                                                   #
#  \param[out]:                                                                  #
##################################################################################
def serial_port_readline(): 
    while 1:
        port.flush()
        data = port.readline()
        print(data)
    
##################################################################################
#  \brief: This function reads the current temperature from the serial port      #
#  \param[in]:                                                                   #
#  \param[out]:                                                                  #
##################################################################################
def serial_port_read_temperature():
    while data != 'exit':
        port.flush()
        data = port.readline()
        print(data)

def main():
    #serial_port_init()
    app = THGDS()
    app.mainloop()

def serial_temperature_request():
    print("requesting temperature to the atmega..\n\r")
    data = 'REQ_'

    #Waiting for request confirmation
    port.flush()
    time.sleep(1)
    #send temperature request to the uC
    port.write('1') 
    time.sleep(1)
    port.flush()
    data = port.readline()
    print(data[12]+data[13]+data[14]+data[15]+data[16] + ' C')



##EVENT HANDLERS       
def temperature_button_event_handler():
    print("temperature button pressed\n\r")
    #serial_temperature_request()
    
def humidity_button_event_handler():
    print("humidity button pressed\n\r")

def gas_button_event_handler():
    print("gas button pressed\n\r")

class THGDS(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(0,weight=1)
        container.grid_columnconfigure(0,weight=1)

        self.wm_title("THGDS")
        self.geometry('350x400')

        selfWidth = self.winfo_reqwidth() 	#get self width
        selfHeight = self.winfo_reqheight()	#get self height

        positionX = int((self.winfo_screenwidth()/2)-(selfWidth))
        positionY = int((self.winfo_screenheight()/2)-(selfHeight))

        self.geometry("+{}+{}".format(positionX, positionY))
        self.resizable(False, False)

        self.frames = {}

        for F in(SerialConnectionPage, StartPage, TemperaturePage, HumidityPage, GasPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame(StartPage)
        #self.mainloop() 

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.configure(background='white')

        lbl_empty = tk.Label(self, text = "        ", bg="white", width = 17, height=2)
        lbl_empty.grid(column = 3, row = 0)
        lbl_title = tk.Label(self, text = "   Temperature, Humidity, and Gas Detection System   ", bg="white", font="Times")
        lbl_title.grid(column = 3, row = 1)
        
        lbl_empty = tk.Label(self, text = "		", bg="white", width = 17, height=2)
        lbl_empty.grid(column = 3, row = 2)
    
        btn1 = tk.Button(self, text = "Temperature Sensor", width = 17, height=1, font="Times",borderwidth=3, command=lambda: controller.show_frame(TemperaturePage))
        btn1.grid(column = 3, row = 5)
        lbl_empty = tk.Label(self, text = "		", bg="white")
        lbl_empty.grid(column = 3, row = 6)
        btn2 = tk.Button(self, text = "Humidity Sensor", width = 17, height=1, font="Times",borderwidth=3,  command=lambda: controller.show_frame(HumidityPage))
        btn2.grid(column = 3, row = 7)
        lbl_empty = tk.Label(self, text = "		", bg="white")
        lbl_empty.grid(column = 3, row = 8)
        btn2 = tk.Button(self, text = "Gas Sensor", width = 17, height=1, font="Times",borderwidth=3, command=lambda: controller.show_frame(GasPage))
        btn2.grid(column = 3, row = 9)

        lbl_empty = tk.Label(self, text = "		", bg="white")
        lbl_empty.grid(column = 3, row = 10)
        btn3 = tk.Button(self, text = "connect to device ", width = 17, height=1, font="Times",borderwidth=3, command=serial_port_init)
        btn3.grid(column = 3, row = 11)


class SerialConnectionPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(background='white')
    
        lbl_empty = tk.Label(self, text = "        ", bg="white", width = 17, height=2)
        lbl_empty.pack(pady=10,padx=10)

        btn1 = tk.Button(self, text = "connect to device ", width = 17, height=1, font="Times",borderwidth=3, command=serial_port_init)
        btn1.pack(pady=10,padx=10)


class TemperaturePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(background='white')
    
        lbl_empty = tk.Label(self, text = "        ", bg="white", width = 17, height=2)
        lbl_empty.pack(pady=10,padx=10)
        #lbl_empty.grid(column = 3, row = 0)
        lbl_title = tk.Label(self, text = " Current temp = ", bg="white", font="Times")
        lbl_title.pack(pady=10,padx=10)
        #lbl_title.grid(column = 3, row = 1)
        lbl_empty = tk.Label(self, text = "        ", bg="white", width = 17, height=2)
        lbl_empty.pack(pady=10,padx=10)
        #lbl_empty.grid(column = 3, row = 2)

        btn1 = tk.Button(self, text = "return home", width = 17, height=1, font="Times",borderwidth=3, command=lambda: controller.show_frame(StartPage))
        btn1.pack(pady=10,padx=10)

class HumidityPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(background='white')
    
        lbl_empty = tk.Label(self, text = "        ", bg="white", width = 17, height=2)
        lbl_empty.pack(pady=10,padx=10)
        #lbl_empty.grid(column = 3, row = 0)
        lbl_title = tk.Label(self, text = " Current Relative Humidty = ", bg="white", font="Times")
        lbl_title.pack(pady=10,padx=10)
        #lbl_title.grid(column = 3, row = 1)
        lbl_empty = tk.Label(self, text = "        ", bg="white", width = 17, height=2)
        lbl_empty.pack(pady=10,padx=10)
        #lbl_empty.grid(column = 3, row = 2)

        btn1 = tk.Button(self, text = "return home", width = 17, height=1, font="Timesffff",borderwidth=3, command=lambda: controller.show_frame(StartPage))
        btn1.pack(pady=10,padx=10)

class GasPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(background='white')
    
        lbl_empty = tk.Label(self, text = "        ", bg="white", width = 17, height=2)
        lbl_empty.pack(pady=10,padx=10)
        #lbl_empty.grid(column = 3, row = 0)
        lbl_title = tk.Label(self, text = " page pending ", bg="white", font="Times")
        lbl_title.pack(pady=10,padx=10)
        #lbl_title.grid(column = 3, row = 1)
        lbl_empty = tk.Label(self, text = "        ", bg="white", width = 17, height=2)
        lbl_empty.pack(pady=10,padx=10)
        #lbl_empty.grid(column = 3, row = 2)

        btn1 = tk.Button(self, text = "return home", width = 17, height=1, font="Times",borderwidth=3, command=lambda: controller.show_frame(StartPage))
        btn1.pack(pady=10,padx=10)

       
main()