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
from colorsLib import colorDictionary
import imageMethods as imgM #Imports all functions needed
file = "images/Default.png"#global variable to keep track of original image file location
image = Image.open("images/Default.png")#global variable to keep track of current image
undo = [] #global stack to keep track of all previous edits
redo = []#global stack to keep track of all previous undo


def main():
    """Main method that initializes the GUI."""
    master = tk.Tk()#Initialize tkinter
    master.configure(bg='grey45') 

    startframe = tk.Frame(master)
    canvas = tk.Canvas(startframe, width=512, height=512)
    canvas.configure(bg='grey30')#Create intial window

    chooseFile(master, canvas) #grab starting file

    #Allows for re-choosing image
    chooseImageButton = tk.Button(master, text="Choose New Image",
                                  command=lambda: chooseFile(master, canvas))
    chooseImageButton.pack()

    #saves current image
    saveImageButton = tk.Button(master, text="Save Image",
                                command=lambda: saveImage(image))

    saveImageButton.pack()

    startframe.pack()
    canvas.pack()

    #array of functions that create effects and filters of images
    Options = ["Invert Color", "Greyscale", "Black and White",
               "Color Scale", "Create Contour", "Add Contrast",
               "Increase Brightness", "Deep Fry","Split Horizontally",
               "Split Vertically", "Fade Image"]
    
    variable = tk.StringVar(master)
    variable.set(Options[0])  # default value

    w = tk.OptionMenu(master, variable, *Options)
    w.pack() #packs all the options in the scrollbar

    confirmOptionsButton = tk.Button(master, text="Confirm",
                                     command=lambda: confirmButton(variable.get(),master, canvas))
    
    confirmOptionsButton.pack()#Creates the confirm button using the confirmButton() function

    resetImageButton = tk.Button(master, text="Reset",
                                 command=lambda: resetImage(master, canvas))
    
    resetImageButton.pack() #Creates the reset button using the resetImage() function

    undoImageButton = tk.Button(master, text="Undo",
                                  command=lambda: undoImage(master, canvas))
    
    undoImageButton.pack()#Creates the Undo button using the undoImage() function

    redoImageButton = tk.Button(master, text="Redo",
                                command=lambda: revertImage(master, canvas))

    redoImageButton.pack()  # Creates the redo button using the revertImage() function

    displayNewImage(master, canvas)

    master.mainloop()
#main()

def chooseFile(master, canvas):
    """Function that allows the user to navigate their directory for a photo.

        Parameters:
                master (tkinter.Tk) = An instance of tkinter.
                canvas (tkinter.Canvas) = A tkinter window.
    """
    global image, undo, file
    master.update()
    file = tk.filedialog.askopenfilename(initialdir="/", title="Select a File",
                                         filetypes=(("JPG files", ".jpg"),
                                                    ("PNG files", ".png"),
                                                    ("JPEG files", ".jpeg")))
    # Selects a file

    if len(file) > 0: #checks to see if file is not null
        image = Image.open(file)
        image.convert("RGBA")
    #if()
    else:
        image = Image.open("images/Default.png")
        file = "images/Default.png"
        image.convert("RGBA")
    #else

    undo.clear()  # clears the undo stack
    undo.append(image)  # adds the base image to the undo stack

    displayNewImage(master, canvas)
#chooseFile()

def saveImage(image):
    """Function that saves the current image when called.

        Parameters:
                image (PIL.Image.Image) = The Image to be saved.
    """
    copy = Image.fromarray(np.asarray(image))
    copy = copy.convert("RGB") #problem with saving in rgba
    filename = filedialog.asksaveasfile(mode='w',defaultextension=".jpg")
    #makes a writable file
    if not filename:
        return
    #if()
    copy.save(filename)#saves the file
#saveImage()

def confirmButton(variable, master, canvas):
    """Function that receives signals from buttons and calls the matching method.

        Parameters:
                variable (str) = A string that holds the chosen option.
                master (tkinter.Tk) = An instance of tkinter.
                canvas (tkinter.Canvas) = A tkinter window.
                
        Returns:
                Nothing.
    """
    global undo, image, file
    copy = Image.fromarray(np.asarray(image))
    originalImage = Image.open(file)
    undo.append(copy)
    redo.clear()
    #else()
    
    if variable == "Invert Color":
        image = imgM.invertColor(copy)
        displayNewImage(master, canvas)
    #if()
    elif variable == "Greyscale":
        image = imgM.greyscale(copy)
        displayNewImage(master, canvas)
    #elif()
    elif variable == "Black and White":
        image = imgM.blackNWhite(copy)
        displayNewImage(master, canvas)
    #elif()
    elif variable == "Create Contour":
        image = imgM.createContour(copy)
        displayNewImage(master, canvas)
    #elif()
    elif variable == "Add Contrast":
        image = imgM.addContrast(copy)
        displayNewImage(master, canvas)
    #elif()
    elif variable == "Increase Brightness":
        image = imgM.addBrightness(copy)
        displayNewImage(master, canvas)
    #elif()
    elif variable == "Deep Fry":
        makeDeepFryWindow(master, canvas)
    #elif()
    elif variable == "Split Horizontally":
        image = imgM.halfNHalfHorizontal(copy, originalImage)
        displayNewImage(master, canvas)
    #elif()
    elif variable == "Split Vertically":
        image = imgM.halfNHalfVertical(copy, originalImage)
        displayNewImage(master, canvas)
    #elif()
    elif variable == "Fade Image":
        image = imgM.fadeFilter(copy, originalImage)
        displayNewImage(master, canvas)
    #elif()
    elif variable == "Color Scale":
        root = tk.Toplevel()
        Options = [ "Red", "Blue", "Green", "Yellow",
                    "Chartreuse", "Cyan", "Magenta",
                    "Transparent"]  #Options for Colorscale function

        variable = tk.StringVar(root)
        variable.set(Options[0])  #default value

        w = tk.OptionMenu(root, variable, *Options)  # create pop up window
        w.pack()

        confirmOptionsButton = tk.Button(root, text="Confirm",
                                         command=lambda: colorScale(root, variable.get(), master, canvas))
        confirmOptionsButton.pack()  # executes the function
    #elif()
#confirmButton()

def displayNewImage(master, canvas):
    """Function that displays the newly edited image on the main window.

        Parameters:
                master (tkinter.Tk) = An instance of tkinter.
                canvas (tkinter.Canvas) = A tkinter window.
    """
    global image
    copy = Image.fromarray(np.asarray(image))
    h,w= copy.size
    if h == w or h > w: #if statement to help resize file to a maximum of (512,512)
        copy = copy.resize((750, int(750*w/h)))
    #if()
    else:
        copy = copy.resize((int(750*h/w), 750))
    #else
    master.geometry(str(copy.size[0] +50) + "x" + str(copy.size[1] + 200))
    canvas.config(width=copy.size[0], height=copy.size[1])  # Configs the window around the image
    master.update()

    one = ImageTk.PhotoImage(copy)
    master.one = one  # to prevent the image garbage collected.

    canvas.create_image((0, 0), image=one, anchor='nw')
#displayNewImage()

def makeDeepFryWindow(master, canvas):
    """Function that creates the option window for the DeepFry function.

        Parameters:
                master (tkinter.Tk) = An instance of tkinter.
                canvas (tkinter.Canvas) = A tkinter window.
    """
    root = tk.Toplevel()
    Options = ["red", "blue", "green"]  # Options for Deepfry function
    variable = tk.StringVar(root)
    variable.set(Options[0])  # default value

    w = tk.OptionMenu(root, variable, *Options)  # create pop up window
    w.pack()

    confirmDeepFryButton = tk.Button(root, text="Okay",
                                     command=lambda: deepFry(root, variable.get(), master, canvas))
    confirmDeepFryButton.pack()  # executes the function
#makeDeepFryWindow()

def deepFry(root, Domcolor, master, canvas):
    """Function that calls the imageMethods deepFry() function.

        Parameters:
                root (tkinter.Toplevel) = A pop up window.
                Domcolor (str) = The selected option for the imgM.deepFry function
                master (tkinter.Tk) = An instance of tkinter.
                canvas (tkinter.Canvas) = A tkinter window.
    """
    global image
    copy = Image.fromarray(np.asarray(image))
    image = imgM.deepFry(copy, Domcolor)
    root.destroy()
    displayNewImage(master, canvas)
#deepFry()

def colorScale(root, color, master, canvas):
    """Function that scales the colors based off of a selected color.

        Scales the image based off a color chosn from the 'Color Scale'
        variable. It then uses colorDictionary to get the associated tuple value.

        Parameters:
                root (tkinter.Toplevel) = A pop up window.
                color (str) = The selected option for the imgM.colorScale function
                master (tkinter.Tk) = An instance of tkinter.
                canvas (tkinter.Canvas) = A tkinter window.
    """
    global image
    copy = Image.fromarray(np.asarray(image))
    if color == "Red":
        image = imgM.colorscale(copy, colorDictionary["Red"])
    #if()
    elif color == "Blue":
        image = imgM.colorscale(copy, colorDictionary["Blue"])
    # elif()
    elif color == "Green":
        image = imgM.colorscale(copy, colorDictionary["Green"])
    # elif()
    elif color == "Yellow":
        image = imgM.colorscale(copy, colorDictionary["Yellow"])
    # elif()
    elif color == "Chartreuse":
        image = imgM.colorscale(copy, colorDictionary["Chartreuse"])
    # elif()
    elif color == "Cyan":
        image = imgM.colorscale(copy, colorDictionary["Cyan"])
    #elif()
    elif color == "Magenta":
        image = imgM.colorscale(copy, colorDictionary["Magenta"])
    #elif()
    elif color == "Transparent":
        image = imgM.colorscale(copy, colorDictionary["Transparent"])
        print("What did you expect?")
    #elif()
        
    root.destroy()
    displayNewImage(master, canvas)
#colorScale()

def resetImage(master, canvas):
    """Function that resets the image to it's original version.

        Parameters:
                master (tkinter.Tk) = An instance of tkinter.
                canvas (tkinter.Canvas) = A tkinter window.
    """
    global image, undo

    undo.append(image)#add the original image to the stack
    image = undo[0]#set the original image as the current image

    displayNewImage(master, canvas)
    #else()
#resetImage()

def undoImage(master, canvas):
    """Function that sets the image back a previous edit.

        Parameters:
                master (tkinter.Tk) = An instance of tkinter.
                canvas (tkinter.Canvas) = A tkinter window.
    """
    global image, undo, redo
    if len(undo) == 1: #check to see if undo stack is empty
        image = undo[0]
    #if()
    else:
        redo.append(image)
        image = undo.pop()  # Set image to top of undo stack


    #else()
    displayNewImage(master, canvas)
#undoImage()

def revertImage(master, canvas):
    """Function that is ctrl+ y to undo's ctrl+z.

            Parameters:
                    master (tkinter.Tk) = An instance of tkinter.
                    canvas (tkinter.Canvas) = A tkinter window.
    """
    global undo, redo, image
    if len(redo) != 0:
        undo.append(image)
        image = redo.pop()  # Set image to top of undo stack
    #if()
    displayNewImage(master, canvas)

if __name__ == "__main__":
    """Calls main function."""
    main()
