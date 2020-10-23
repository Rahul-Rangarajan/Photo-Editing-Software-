'''
Contributors:
    Jack Castiglione
    Rahul Rangarajan
    Cameron King
    Nick Jonas
'''

import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog
import os
import imageMethods as imgM
import colorsLib as colors
filename = " "

def main():
    print("Hi")
    master = tk.Tk()
    chooseFile()
    chooseImageButton = tk.Button(master, text="Choose New Image", command=chooseFile)
    chooseImageButton.pack()

    image = Image.open(filename)

    #saveImageButton = tk.Button(master, text="Save Image", command=image.save("images/editedLeia.jpg"))
    #saveImageButton.pack()

    variable = tk.StringVar(master)
    variable.set("Choose a Filter")  # default value

    w = tk.OptionMenu(master, variable, "Deepfry", "Greyscale", "Black and White")
    w.pack()

    print(filename)

    master.mainloop()
    #Where the image should be saved, by default is the same directory
    #that this file is in
    #path, filename = os.path.split(os.path.abspath(__file__))
    #print(filename)

def chooseFile():
    file = tk.filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("Text files", "*.txt*"), ("all files", "*.*")))
    global filename
    filename = file








if __name__ == "__main__":
    main()
