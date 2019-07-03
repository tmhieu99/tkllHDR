from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from time import sleep
from keras.datasets import mnist 
from keras.utils import np_utils
import cv2
import serial
import datetime
import matplotlib.pyplot as plt 
import numpy as np
import glob
import sys

INPUT_SIZE  = 14
BUTTON_H    = 2
BUTTON_W    = 20
X           = 10
Y           = 10
INPUT_SIZE  = (14, 14)
IMG_SIZE    = (180, 180)

class Picture:
    def __init__(self, image_name, greyscale = True):
        self.image_cv = cv2.imread(image_name, 0)
        self.image_cv = image_processing(self.image_cv)

        # Record result
        t = datetime.datetime.now()
        filename = "../../data/result"
        for i in [t.day, t.month, t.year, t.hour, t.minute, t.second, 'jpg']:
            filename += '.' + str(i)
        cv2.imwrite(filename, self.image_cv)
        self.image_cv = cv2.imread(filename, 0)

        print(self.image_cv)

        self.image_tk = cv2.imread(image_name, not greyscale)
        self.image_tk = cv2.resize(self.image_tk, IMG_SIZE, interpolation = cv2.INTER_AREA)
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

def push_test():
    # Load MNIST data
    (x1, y_train), (x2, y_test) = mnist.load_data()
    x_train = np.array([cv2.resize(x1[i], (INPUT_SIZE, INPUT_SIZE), interpolation = cv2.INTER_AREA) for i in range(len(x1))])
    x_test = np.array([cv2.resize(x2[i], (INPUT_SIZE, INPUT_SIZE), interpolation = cv2.INTER_AREA) for i in range(len(x2))])
    num_classes = 10
    
    # Normalize inputs from 0-255 to 0-1
    x_train = x_train / 255
    x_test = x_test / 255
    
    # One hot encode outputs
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)
    
    # Flatten
    x_train = x_train.reshape(x_train.shape[0], INPUT_SIZE*INPUT_SIZE).astype('float32')
    x_test = x_test.reshape(x_test.shape[0], INPUT_SIZE*INPUT_SIZE).astype('float32')

    # Get picture data in matrix form
    data = x_train
    
    # Flatten the matrix to a 1D-vector 784 long
    #data = data.reshape(data.shape[0]*data.shape[1])
    
    # Convert list to string with leading zeros to fit the data data format
    converted_data = ''
    for i in range(len(data)):
        if i != 0: converted_data = converted_data + ","
        converted_data = converted_data + str(data[i])

    # Convert to byte string
    converted_data = converted_data.encode('ascii') + b'\n'

    #print(converted_data)

    # Send data to Zedboard

    correct = 0
    for i in range (10000):
        ser.write(converted_data[196*i:196*i+195])
        predict = ser.readline()
        if predict[len(predict)-2] == y_test[i]:
            correct += 1

    accuracy = correct / 10000

def crop_image(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    region = (0, 0, 0, 0)
    max_area = 0
    for cont in contours:
        x, y, w, h = cv2.boundingRect(cont)
        area = w*h
        if area > max_area:
            region = x,y,w,h
            max_area = area
    x, y, w, h = region
    
    roi = img[y:y+h,x:x+w]

    size = int(max(w, h)*1.4)
    x2 = (size - w)//2
    y2 = (size - h)//2
    res = np.zeros((size, size))
    res[y2:y2+h, x2:x2+w] = roi
    return res

def image_processing(res):
    # Blur image
    res = cv2.GaussianBlur(res,(9, 9), 1) 

    # Noise reduction
    res = cv2.fastNlMeansDenoising(res, res, 3, 7, 21)
    
    # Apply adaptive thresholding
    res = cv2.adaptiveThreshold(res, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Inverse image
    res = cv2.bitwise_not(res, res)

    # Remove white blobs
    kernel = np.ones((2, 2), np.uint8)
    res = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel)

    # Crop image
    res = crop_image(res)
    
    # Dilate image
    kernel = np.ones((5, 5), np.uint8)
    res = cv2.dilate(res,kernel,iterations = 1)

    # Scale image
    res = cv2.resize(res, INPUT_SIZE, interpolation = cv2.INTER_AREA)
    
    # Final result
    return res

def import_image():
    filename = askopenfilename( initialdir = "../../data/raw",
                                initialfile = "",
                                filetypes = (("All Files", "*"),
                                            ("Text File", "*.txt")),
                                title = "Choose image")
    if len(filename) > 0:
        global subject 
        global image
        subject = Picture(filename, greyscale.get())
        image.config(image = subject.obj())
  
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
    x = ser.readline()

    # Show result on screen
    update_text(x)

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

class App(Frame):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        self.master.title("Windows")
        self.pack(fill=BOTH, expand=True)

        self.columnconfigure(1, weight=10)
        self.columnconfigure(3, pad=5)
        self.rowconfigure(3, weight=10)
        self.rowconfigure(5, pad=5)

        global port_menu
        global image
        port_menu       = OptionMenu(self, selected_port, *port_list)
        b_import        = Button(self, text='Import image', command=import_image)
        b_push          = Button(self, text='Push image', command=lambda:push_image(ser))
        b_evaluation    = Button(self, text='Evaluation', command=push_test)
        gs_cbutton      = Checkbutton(self, text='Grayscale', variable=greyscale)
        image           = Label(self)
        text            = Text(self)
        frame           = Frame(self) 

        port_menu.config(bg = 'white', width=BUTTON_W*90//100)
        port_menu.bind("<Button-1>", update_ports)
        gs_cbutton.select()
        b_import.config(bg='white', width=BUTTON_W, height=BUTTON_H)
        b_push.config(bg='white', width=BUTTON_W, height=BUTTON_H)
        b_evaluation.config(bg='white', width=BUTTON_W, height=BUTTON_H)


        port_menu.      grid(row=0, column=0, padx=X, pady=Y)
        b_import.       grid(row=1, column=0, padx=X)
        b_push.         grid(row=2, column=0, padx=X)
        b_evaluation.   grid(row=3, column=0, padx=X, pady=15, sticky=N)
        gs_cbutton.     grid(row=4, column=0, padx=X, sticky=N)
        image.          grid(row=5, column=0, padx=X, pady=Y)
        text.           grid(row=0, column=1, rowspan=6, pady=Y, sticky=E+W+S+N)
        frame.          grid(row=0, column=2, rowspan=5, padx=X//2)

# Setup window
root = Tk()
root.geometry("760x500")
root.resizable(False, False)

# Variables
ser = None
greyscale = BooleanVar()
port_list = available_ports()
selected_port = StringVar(root)
selected_port.set(port_list[0])
ser = connect(selected_port.get()) 

app = App()
root.mainloop()
