import cv2
import numpy as np
import datetime
import matplotlib.pyplot as plt 
from tkinter import *
from tkinter.filedialog import askopenfilename

def open_image():
    filename = askopenfilename( initialdir = "./",
                                initialfile = "",
                                filetypes = (("JPG", "*.jpg"), ("All Files", "*.*")),
                                title = "Choose an image")
    if len(filename) > 0:
        img = cv2.imread(filename, 0)
        res = image_processing(img)
        show_result(img, res)

def crop_image(img):
    for top in range(len(img)): 
        if any(img[top]): break
    for bot in range(len(img)-1, -1, -1): 
        if any(img[bot]): break;
    for left in range(len(img[0])): 
        if any(img[:, left]): break;
    for right in range(len(img[0])-1, -1, -1): 
        if any(img[:, right]): break;

    spacing = int(max(bot-top, right-left)*0.25)

    top, left  = [(i - spacing if i > spacing else 0) for i in [top, left]]
    bot, right = [(i + spacing if i + spacing < j else j) for i, j in [(bot, len(img)), (right, len(img[0]))]]

    img = img[top:bot, left:right]

    return img

def image_processing(res):
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
    
    # Scale image
    res = cv2.resize(res, (28, 28), interpolation = cv2.INTER_AREA)
    
    # Final result
    return res
    
def show_result(ori, res):
    # Record result
    t = datetime.datetime.now()
    filename = "./res/result"
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
    root.title("Image preprocessing")
    root.geometry("250x250")
    root.resizable(False,False)

    button = Button(root, text = "Select image", command = open_image)
    button.pack(fill = BOTH, expand = 1)

    root.mainloop()
