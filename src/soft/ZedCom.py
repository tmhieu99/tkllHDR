from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from time import sleep
import cv2
import serial
import numpy as np
import glob
import sys

MARGIN_L        = 10
MARGIN_T        = 10
BUTTON_HEIGHT   = 2
BUTTON_WIDTH    = 20
CBUTTON_HEIGHT  = 2
CBUTTON_WIDTH   = 17
TEXTBOX_HEIGHT  = 22
TEXTBOX_WIDTH   = 50
MENU_HEIGHT     = 1
MENU_WIDTH      = 15

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
    if len(result) == 0: result.append("None")
    return result

def import_image():
    filename = askopenfilename( initialdir = "../data/",
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
  
def update_text(data):
    print(data)
    data = data.decode('utf-8')
    text.insert(END, data)

def push_image(ser):
    # Get picture data in matrix form
    data = subject.mat()

    # Flatten the matrix to a 1D-vector 784 long
    data = data.reshape(data.shape[0]*data.shape[1])

    # Convert list to string with leading zeros to fit the data data format
    converted_data = ''
    for i in range(len(data)):
        if i != 0: converted_data = converted_data + ","
        converted_data = converted_data + str(data[i])

    # Convert to byte string
    converted_data = converted_data.encode('ascii') + b'\n'

    print(converted_data)
    # Send data to Zedboard
    ser.write(converted_data)

    # Wait for result
    #x = ser.readline()
    #x = ser.readlines()

    # Show result on screen
    #update_text(x)

def connect(port):
    if port == "None": return
    try:
        ser = serial.Serial(port, 115200, timeout = 1)
        return ser
    except:
        print("Error occured while connecting to selected port. Please try again.")

def update_ports(event):
    try: ser.close()
    except: pass
    port_list = available_ports()
    tmp = port_menu["menu"]
    tmp.delete(0, "end")
    for port in port_list: tmp.add_command(label = port)
    selected_port.set(port_list[0])
    ser = connect(selected_port.get())

def new_menu(root, x, y, selected_port, port_list, cmd, w = MENU_WIDTH, h = MENU_HEIGHT, bg = 'white'):
    menu = OptionMenu(root, selected_port, *port_list)
    menu.config(bg = bg, width = w, height = h)
    menu.bind("<Button-1>", cmd)
    menu.place(x = x, y = y)
    return menu

def new_image(root, x, y):
    image = Label(root)
    image.place(x = x, y = y)
    return image

def new_textbox(root, x, y, w = TEXTBOX_WIDTH, h = TEXTBOX_HEIGHT):
    textbox = Text(root, width = TEXTBOX_WIDTH, height = TEXTBOX_HEIGHT)
    textbox.place(x = x, y = y)
    return textbox

def new_button(root, x, y, txt, cmd, w = BUTTON_WIDTH, h = BUTTON_HEIGHT, bg = 'white'):
    button = Button(root, width = w, height = h, bg = bg, text = txt, command = cmd)
    button.place(x = x, y = y)
    return button

def new_checkbutton(root, x, y, txt, var, w = CBUTTON_WIDTH, h = CBUTTON_HEIGHT):
    checkbutton = Checkbutton(root, width = w, height = h, variable = var, text = txt)
    checkbutton.place(x = x, y = y)
    checkbutton.select()
    return checkbutton

if __name__ == "__main__":
    # Setup window
    root = Tk()
    root.title('Zedboard Communicator')
    root.geometry('635x400')
    root.resizable(False, False)
    
    # Variables
    ser = None
    greyscale = BooleanVar()
    port_list = available_ports()
    selected_port = StringVar(root)
    selected_port.set(port_list[0])
    ser = connect(selected_port.get()) 
     
    # Widgets
    port_menu   = new_menu(root, MARGIN_L-3, MARGIN_T-1, selected_port, port_list, update_ports)
    b_import    = new_button(root, MARGIN_L, 60, 'Import image', import_image)
    b_push      = new_button(root, MARGIN_L, 110, 'Push image', lambda: push_image(ser))
    gs_cbutton  = new_checkbutton(root, MARGIN_L, 160, 'Greyscale', greyscale)
    image       = new_image(root, 70, 220)
    text        = new_textbox(root, 170, MARGIN_T)
    
    # Main loop
    root.mainloop()
