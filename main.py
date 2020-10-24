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
stack = []


def main():
    print("Hi")
    master = tk.Tk()
    master.configure(bg='grey45')

    startframe = tk.Frame(master)
    canvas = tk.Canvas(startframe, width=512, height=512)
    canvas.configure(bg='grey30')


    chooseFile(master, canvas)

    #Allows for re-choosing image
    chooseImageButton = tk.Button(master, text="Choose New Image", command=lambda: chooseFile(master, canvas))
    chooseImageButton.pack()

    #saves current image
    saveImageButton = tk.Button(master, text="Save Image", command=lambda: saveImage(image))
    saveImageButton.pack()

    startframe.pack()
    canvas.pack()

    #array of functions that create effects and filters of images
    Options = ["Invert Color", "Greyscale", "Black and White", "Create Contour",
               "Add Contrast", "Increase Brightness", "Deep Fry",
               "Split Horizontally", "Split Vertically", "Fade Image", "Comic Book"]
    variable = tk.StringVar(master)
    variable.set(Options[0])  # default value

    w = tk.OptionMenu(master, variable, *Options)
    w.pack()

    confirmOptionsButton = tk.Button(master, text="Confirm", command=lambda: confirmButton(variable.get(),master, canvas))
    confirmOptionsButton.pack()

    resetImageButton = tk.Button(master, text="Reset", command=lambda: resetImage(master, canvas))
    resetImageButton.pack()

    revertImageButton = tk.Button(master, text="Undo", command=lambda: revertImage(master, canvas))
    revertImageButton.pack()

    displayNewImage(startframe, canvas)

    master.mainloop()

def chooseFile(master, canvas):
    file = tk.filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("JPG files", ".jpg"), ("PNG files", ".png"),
                                                                                           ("JPEG files", ".jpeg")))
    global image, originalImage, stack
    image = Image.open(file)
    image.convert("RGBA")
    originalImage = Image.open(file)
    originalImage.convert("RGBA")
    h, w = image.size
    if h == w or h > w:
        image = image.resize((512, int(512*w/h)))
        originalImage = originalImage.resize((512, int(512 * w / h)))
    else:
        image = image.resize((int(512*h/w), 512))
        originalImage = originalImage.resize((int(512 * h / w), 512))
    master.geometry(str(image.size[0] + 50) + "x" + str(image.size[1]+200))
    canvas.config(width=image.size[0], height=image.size[1])
    stack = []
    displayNewImage(master, canvas)
#chooseFile()

def saveImage(image):
    files = [('Image Files', '*.*')]
    file = tk.filedialog.asksaveasfile(filetypes=files, defaultextension=files)
#saveImage()

def confirmButton(variable, master, canvas):
    global stack, image
    stack.append(image)
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
    elif variable == "Fade Image":
        image = imgM.fadeFilter(image, originalImage)
        displayNewImage(master, canvas)
    elif variable == "Comic Book":
        image = imgM.comicBook(image)
        displayNewImage(master, canvas)
#confirmButton()

def displayNewImage(master, canvas):
    global image
    copy = image
    w,h = image.size
    one = ImageTk.PhotoImage(copy)
    master.one = one  # to prevent the image garbage collected.
    canvas.create_image((0, 0), image=one, anchor='nw')
#displayNewImage()

def deepFry(root, Domcolor, master, canvas):
    global image
    image = imgM.deepFry(image, Domcolor)
    root.destroy()
    displayNewImage(master, canvas)
#deepFry()

def resetImage(master, canvas):
    global image, originalImage
    image = originalImage
    displayNewImage(master, canvas)
#resetImage()
def revertImage(master, canvas):
    global originalImage, image, stack
    if len(stack) == 0:
        image = originalImage
    else:
        latest = len(stack)-1
        image = stack[latest]
        stack.remove(stack[latest])

    displayNewImage(master, canvas)
#revertImage()
if __name__ == "__main__":
    main()
