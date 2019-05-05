from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import cv2
import serial
import numpy as np
import glob
import sys


def Picture(image_name, greyscale = True):
    image = cv2.imread(image_name, not greyscale)
    if not greyscale:
        b, g, r = cv2.split(image)
        image = cv2.merge((r, g, b))
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image=image)
    return image
def available_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
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
if __name__ == "__main__":
    def import_image():
        filename = askopenfilename( initialdir = "./",
                                    initialfile = "",
                                    filetypes = (("All Files", "*"),
                                                ("Text File", "*.txt")),
                                    title = "Choose image")
        if len(filename) > 0:
            global img
            global image
            img = Picture(filename, greyscale.get())
            image.config(image = img)
  
    def push_image():
        img = img.reshape(img.shape[0]*img.shape[1])
        ser = serial.Serial(port='', baudrate=115200)
        ser.write(img)
        
    def updatePort(chosenPort):
        try:
            s = serial.Serial(chosenPort)
            s.close()
        except (OSError, serial.SerialException):
            listPorts = available_ports()
            
    # Setup window
    root = Tk()
    root.config(bg = 'white')
    root.title('Display opencv image')
    root.geometry('500x500')
    root.resizable(False, False)

    # Variables
    greyscale = BooleanVar()
    option = StringVar(root)
    ports = available_ports()
    if len(ports) == 0: ports.append("None")
    option.set(ports[0])
    
    # Port list
    listPorts = available_ports()
    optionMenu = OptionMenu(root, option, *listPorts, command=updatePorts)
    optionMenu.grid(row=2, column=0)

    # Display result
    result = 5
    text = Text(root, width=20, height=10, font=("Helvetica", 25))
    text.insert('1.0', 'Result: ')
    text.insert('2.0', result)
    
    # Widgets
    image       = Label(root)
    b_import    = Button(root, bg = 'white', text = 'Import image', command = import_image, font=("Helvetica", 19))
    b_greyscale = Checkbutton(root, bg = 'white', variable = greyscale, text = 'Greyscale', font=("Helvetica", 19))
    b_greyscale.select()
    b_push = Button(root, bg='white', text='Push', command = push_image)

    # Positioning
    optionMenu.grid(row=0, column=0)
    b_import.grid(row = 0, column = 1)
    b_push.grid(row=0, column = 2, sticky = W)
    b_greyscale.grid(row = 0, column = 3)
    image.grid(row = 1, column = 0, columnspan = 2, sticky = W) 

    # Main loop
    root.mainloop()
