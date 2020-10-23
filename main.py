'''
Contributors:
    Jack Castiglione
    Rahul Rangarajan
    Cameron King
    Nick Jonas
'''

import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
import os
import imageMethods as imgM
import colorsLib as colors
image = Image.open("images/Leia.jpg")
originalImage = Image.open("images/Leia.jpg")


def main():
    print("Hi")
    master = tk.Tk()
    master.geometry("562x700")

    chooseFile()

    #Allows for re-choosing image
    chooseImageButton = tk.Button(master, text="Choose New Image", command=lambda: chooseFile())
    chooseImageButton.pack()

    #saves current image
    saveImageButton = tk.Button(master, text="Save Image", command=lambda: saveImage(image))
    saveImageButton.pack()

    startframe = tk.Frame(master)
    canvas = tk.Canvas(startframe, width=512, height=512)
    startframe.pack()
    canvas.pack()

    #array of functions that create effects and filters of images
    Options = ["Invert Color", "Greyscale", "Black and White", "Create Contour",
               "Add Contrast", "Increase Brightness", "Deep Fry",
               "Split Horizontally", "Split Vertically"]
    variable = tk.StringVar(master)
    variable.set(Options[0])  # default value

    w = tk.OptionMenu(master, variable, *Options)
    w.pack()

    confirmOptionsButton = tk.Button(master, text="Confirm", command=lambda: confirmButton(variable.get(),master, canvas))
    confirmOptionsButton.pack()

    resetImageButton = tk.Button(master, text="Reset", command=lambda: resetImage(master, canvas))
    resetImageButton.pack()

    displayNewImage(startframe, canvas)

    master.mainloop()
    #Where the image should be saved, by default is the same directory
    #that this file is in
    #path, filename = os.path.split(os.path.abspath(__file__))
    #print(filename)

def chooseFile():
    file = tk.filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("JPG files", "*.jpg*"), ("PNG files", "*.png*"),
                                                                                           ("JPEG files", "*.jpeg*")))
    global image
    global originalImage
    image = Image.open(file)
    originalImage = Image.open(file)
    h,w = image.size
    if h==w or h>w:
        image = image.resize((512 , int(512*w/h)))
        originalImage = originalImage.resize((512, int(512 * w / h)))
    else:
        image = image.resize((int(512*h/w) , 512))
        originalImage = originalImage.resize((int(512 * h / w), 512))



#chooseFile()

def saveImage(image):
    image.save("images2/Leia Edited.jpg")
#saveImage()

def confirmButton(variable, master, canvas):
    global image
    if variable == "Invert Color":
        image = imgM.invertColor(image)
        displayNewImage(master, canvas)
    elif variable == "Greyscale":
        image = imgM.greyscale(image)
        displayNewImage(master, canvas)
    elif variable == "Black and White":
        image = imgM.blackNWhite(image)
        displayNewImage(master, canvas)
    elif variable == "Create Contour":
        image = imgM.createContour(image)
        displayNewImage(master, canvas)
    elif variable == "Add Contrast":
        image = imgM.addContrast(image)
        displayNewImage(master, canvas)
    elif variable == "Increase Brightness":
        image = imgM.addBrightness(image)
        displayNewImage(master, canvas)
    elif variable == "Deep Fry":
        root = tk.Toplevel()

        Options = ["red", "blue", "green"]
        variable = tk.StringVar(root)
        variable.set(Options[0])  # default value

        w = tk.OptionMenu(root, variable, *Options)
        w.pack()

        confirmOptionsButton = tk.Button(root, text="Confirm",
                                         command=lambda: deepFry(root, variable.get(), master, canvas))
        confirmOptionsButton.pack()
    elif variable == "Split Horizontally":
        image = imgM.halfNHalfHorizontal(image, originalImage)
        displayNewImage(master, canvas)
    elif variable == "Split Vertically":
        image = imgM.halfNHalfVertical(image, originalImage)
        displayNewImage(master, canvas)
#confirmButton()

def displayNewImage(master, canvas):
    print("displaying")
    one = ImageTk.PhotoImage(image)
    master.one = one  # to prevent the image garbage collected.
    canvas.create_image((0, 0), image=one, anchor='nw')
#displayNewImage()

def deepFry(root, Domcolor, master, canvas):
    global image
    print(Domcolor)
    image = imgM.deepFry(image, Domcolor)
    root.destroy()
    displayNewImage(master, canvas)
#deepFry()

def resetImage(master, canvas):
    global image
    global originalImage
    image = originalImage
    displayNewImage(master, canvas)

if __name__ == "__main__":
    main()
