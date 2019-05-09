from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from time import sleep
import cv2
import serial
import numpy as np
import glob
import sys

class Picture:
    def __init__(self, image_name, greyscale = True):
        self.image_cv = cv2.imread(image_name, 0)
        self.image_tk = cv2.imread(image_name, not greyscale)
        if not greyscale:
            b, g, r = cv2.split(self.image_tk)
            self.image_tk = cv2.merge((r, g, b))
        self.image_tk = Image.fromarray(self.image_tk)
        self.image_tk = ImageTk.PhotoImage(image = self.image_tk)

    def mat(self):
        return self.image_cv

    def obj(self):
        return self.image_tk

def available_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def import_image():
    filename = askopenfilename( initialdir = "./",
                                initialfile = "",
                                filetypes = (("All Files", "*"),
                                            ("Text File", "*.txt")),
                                title = "Choose image")
    if len(filename) > 0:
        try:
            global subject 
            global image
            subject = Picture(filename, greyscale.get())
            image.config(image = subject.obj())
        except:
            print("Invalid image type")
  
def push_image():
    data = subject.mat()
    data = list(data.reshape(data.shape[0]*data.shape[1]))
    ser.flush()
    ser.flushInput()
    ser.flushOutput()
    ser.write(data)
    print("-----------------------")
    cnt = 0
    while ser.inWaiting():
        s = ser.readline()
        s = s.decode()[:len(s)-2]
        #print(s, end = '')
        print("%3s" % (s), end = '')
        cnt += 1
        if cnt == 28:
            print()
            cnt = 0

        '''
        text.insert(END, s + " ")
        '''

def connect():
    try:
        global ser
        ser = serial.Serial(port = selected_port.get(),
                            baudrate = 115200,
                            timeout = 1)
    except:
        print("Error occured while connecting to selected port. Please try again.")

def update_ports(event):
    port_list = available_ports()
    tmp = port_menu["menu"]
    tmp.delete(0, "end")
    if len(port_list) == 0: port_list.append("None")
    for port in port_list: tmp.add_command(label = port)
    selected_port.set(port_list[0])
    connect()

if __name__ == "__main__":
    ser = None

    # Setup window
    root = Tk()
    root.config(bg = 'white')
    root.title('Zedboard communicator')
    root.geometry('500x500')
    #root.resizable(False, False)

    # Variables
    greyscale = BooleanVar()
    selected_port = StringVar(root)
    port_list = available_ports()
    if len(port_list) == 0: port_list.append("None")
    selected_port.set(port_list[0])
    connect() 
    
    # Widgets
    port_menu   = OptionMenu(root, selected_port, *port_list)
    port_menu.config(bg = "white", width = 10)
    port_menu.bind("<Button-1>", update_ports)

    image       = Label(root)
    text        = Text(root, width = 30, height = 18)
    b_import    = Button(root, bg = 'white', text = 'Import image', command = import_image)
    b_greyscale = Checkbutton(root, bg = 'white', variable = greyscale, text = 'Greyscale')
    b_push      = Button(root, bg = 'white', text = 'Push', command = push_image)

    b_greyscale.select()

    # Positioning
    port_menu.grid(row = 0, column = 0)
    b_import.grid(row = 0, column = 1)
    b_push.grid(row = 0, column = 2, sticky = W)
    b_greyscale.grid(row = 0, column = 3)
    image.grid(row = 1, column = 0, sticky = W) 
    text.grid(row = 1, column = 1)

    # Main loop
    root.mainloop()
