import cv2
import numpy as np
import datetime
import matplotlib.pyplot as plt 
from tkinter import *
from tkinter.filedialog import askopenfilename

def open_image():
    filename = askopenfilename( initialdir = "../../data/raw",
                                initialfile = "",
                                filetypes = (("JPG", "*.jpg"), ("All Files", "*.*")),
                                title = "Choose an image")
    if len(filename) > 0:
        img = cv2.imread(filename, 0)
        res = image_processing(img)
        show_result(img, res)

def crop_image(img):
    img, contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
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
    res = cv2.resize(res, (14, 14), interpolation = cv2.INTER_AREA)
    
    # Final result
    return res
    
def show_result(ori, res):
    # Record result
    t = datetime.datetime.now()
    filename = "../../data/result"
    for i in [t.day, t.month, t.year, t.hour, t.minute, t.second, 'jpg']:
        filename += '.' + str(i)
    cv2.imwrite(filename, res)

    # Show original, resulted images
    fig = plt.figure(figsize = (5, 5))
    img1 = fig.add_subplot(2, 2, 1)
    img1.imshow(ori, cmap = 'gray')
    img2 = fig.add_subplot(2, 2, 2)
    img2.imshow(res, cmap = 'gray')
    plt.show()

if __name__ == "__main__":
    root = Tk()
    root.title("ZedCom")
    root.geometry("250x250")
    root.resizable(False,False)

    button = Button(root, text = "Select image", command = open_image)
    button.pack(fill = BOTH, expand = 1)

    root.mainloop()
