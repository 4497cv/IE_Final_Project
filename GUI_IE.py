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

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import(FigureCanvasTkAgg, NavigationToolbar2TkAgg)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import numpy as np
import matplotlib.animation as animation
from matplotlib import style
import matplotlib.pyplot as plt


temp_fig = Figure(figsize=(5,4), dpi=60)
t = np.arange(0,3,.01)
ax1= temp_fig.add_subplot(111)
temp_count = 0

hum_fig = Figure(figsize=(5,4), dpi=60)
t = np.arange(0,3,.01)
ax2= temp_fig.add_subplot(111)
hum_count = 0


#                               GUI Functions

##################################################################################
#  \brief:      This function intializes the serial port communication           #
#  \param[in]:                                                                   #
#  \param[out]:                                                                  #
##################################################################################
def serial_port_init():
    serial_port_id = ['/dev/ttyUSB0','/dev/ttyUSB1']
    global port
    try:
        port = Serial(serial_port_id[0], 115200, timeout=0)
        print("conncted to " + serial_port_id[0] + "\n\r")
    except:
        print("serial port "+ serial_port_id[0] + " is not available\n\r")
        try:
            port = Serial(serial_port_id[1], 115200, timeout=0)
            print("conncted to " + serial_port_id[1] + "\n\r")
        except:
            print("serial port "+ serial_port_id[1] + " is not available\n\r")
            print("closing program..\n\r")
            sys.exit()
        

def strisfloat(s):
    try:
        float(s)
        return True
    except:
        return False

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

def serial_temperature_request():
    global temp_count
    f = open('temp_data.txt', 'a+')
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
    print(data)

    temp_count = temp_count+1

    f.write(str(temp_count))
    f.write(',')
    f.write(data[12]+data[13]+data[14]+data[15])
    f.write('\n')

def serial_humidity_request():
    global hum_count
    # f = open('hum_data.txt', 'a+')
    # print("requesting humidity to the atmega..\n\r")
    # data = 'REQ_'
    # #Waiting for request confirmation
    # port.flush()
    # time.sleep(1)
    # #send temperature request to the uC
    # port.write('2') 
    # time.sleep(1)
    # port.flush()
    # data = port.readline()
    # print(data)
    
    # hum_count = hum_count+1

    # f.write(str(hum_count))
    # f.write(',')
    # f.write(data[12]+data[13]+data[14]+data[15])
    # f.write('\n')


def animate_temp(i):
    global hum_count
    serial_temperature_request()
    graph_data = open('temp_data.txt', 'r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x,y = line.split(',')
            xs.append(float(x))
            ys.append(float(y))
    ax1.clear()
    ax1.plot(xs,ys,'r')
    ax1.set_xlabel('Seconds', fontsize=12)
    ax1.set_ylabel('Temperature (C)', fontsize=12)
    ax1.set(xlim=(1,temp_count), ylim=(0,float(y)+10))
    print('refreshing graph...\r\n')

def animate_hum(i):
    serial_humidity_request()
    # graph_data = open('temp_data.txt', 'r').read()
    # lines = graph_data.split('\n')
    # xs = []
    # ys = []
    # for line in lines:
    #     if len(line) > 1:
    #         x,y = line.split(',')
    #         xs.append(float(x))
    #         ys.append(float(y))
    # ax2.clear()
    # ax2.plot(xs,ys,'r')
    # ax2.set_xlabel('Seconds', fontsize=12)
    # ax2.set_ylabel('Relative Humidity (RH)', fontsize=12)
    # ax2.set(xlim=(1,hum_count), ylim=(0,float(y)+10))
    # print('refreshing graph...\r\n')

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
        lbl_title = tk.Label(self, text = "   Temperature, Humidity, and Gas Detection System", bg="white", font="Times")
        lbl_title.grid(column = 3, row = 1)
        
        lbl_empty = tk.Label(self, text = "		", bg="white", width = 17, height=5)
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
    
        #lbl_empty.grid(column = 3, row = 0)
        lbl_title = tk.Label(self, text = "Temperature", bg="white", font="Times")
        lbl_title.pack(pady=10,padx=10)

        canvas = FigureCanvasTkAgg(temp_fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10,padx=10)

        toolbar=NavigationToolbar2TkAgg(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(pady=10,padx=10)

        ani = animation.FuncAnimation(temp_fig, animate_temp, interval=1000)
        canvas.draw()
        btn1 = tk.Button(self, text = "return home", width = 17, height=1, font="Times",borderwidth=3, command=lambda: controller.show_frame(StartPage))
        btn1.pack(pady=10,padx=10)

class HumidityPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.configure(background='white')
    
        #lbl_empty.grid(column = 3, row = 0)
        lbl_title = tk.Label(self, text = "Relative Humidity", bg="white", font="Times")
        lbl_title.pack(pady=10,padx=10)

        canvas = FigureCanvasTkAgg(hum_fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10,padx=10)

        toolbar=NavigationToolbar2TkAgg(canvas,self)
        toolbar.update()
        canvas._tkcanvas.pack(pady=10,padx=10)

        ani = animation.FuncAnimation(hum_fig, animate_hum, interval=10000)
        canvas.draw()
        btn1 = tk.Button(self, text = "return home", width = 17, height=1, font="Times",borderwidth=3, command=lambda: controller.show_frame(StartPage))
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


def main():
    f1 = open('temp_data.txt', 'w+')
    f1.close()
    f2 = open('hum_data.txt', 'w+')
    f2.close()
    f3 = open('gas_data.txt', 'w+')
    f3.close()
    serial_port_init()
    app = THGDS()
    app.mainloop()

main()