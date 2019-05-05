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

def image_processing(res):
    # Noise reduction
    res = cv2.fastNlMeansDenoising(res, res, 3, 7, 21)
    
    # Apply adaptive thresholding
    res = cv2.adaptiveThreshold(res, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    
    # Inverse image
    res = cv2.bitwise_not(res, res)
    
    # Crop image
    for i in range(len(res)):
        if any(res[i]):
            res = res[i:len(res)]
            break
    
    for i in range(len(res)-1, -1,-1):
        if any(res[i]):
            res = res[0:i+1]
            break
    
    for i in range(len(res[0])):
        if any(res[:, i]):
            res = res[:, i:len(res[0])]
            break
    
    for i in range(len(res[0])-1, -1,-1):
        if any(res[:, i]):
            res = res[:, 0:i+1]
            break
    
    size = max(res.shape[0], res.shape[1])
    bg = np.zeros((size, size))
    
    if res.shape[0] > res.shape[1]:
        s = ((res.shape[0] - res.shape[1])//2) 
        bg[:, s:(s+res.shape[1])] = res
        res = bg
    else:
        s = ((res.shape[1] - res.shape[0])//2) 
        bg[s:(s+res.shape[0]), :] = res
        res = bg
    
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
