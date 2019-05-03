from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import cv2
import numpy as np

def Picture(image_name, greyscale = True):
    image = cv2.imread(image_name, not greyscale) 
    if not greyscale:
        b, g, r = cv2.split(image)
        self.image = cv2.merge((r, g, b))
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image=image) 
    return image

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
            image = Label(root, image = img)
            image.grid(row = 1, column = 0, columnspan = 2, sticky = W) 

    # Setup window
    root = Tk()
    root.config(bg = 'white')
    root.title('Display opencv image')
    root.geometry('500x500')
    root.resizable(False, False)

    greyscale = BooleanVar()

    # Widgets
    b_import    = Button(root, bg = 'white', text = 'Import image', command = import_image)
    b_greyscale = Checkbutton(root, bg = 'white', variable = greyscale, text = 'Greyscale')
    b_greyscale.select()

    # Positioning
    b_import.grid(row = 0, column = 0)
    b_greyscale.grid(row = 0, column = 1)

    # Main loop
    root.mainloop()
