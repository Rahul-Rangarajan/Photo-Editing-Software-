'''
Contributors:
    Jack Castiglione
    Rahul Rangarajan
    Cameron King
    Nick Jonas
'''

from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from colorsLib import chartreuse, cyan, red, green, magenta, yellow, blue
import imageMethods as imgM #Imports all functions needed
file = "images/Default.png"#global variable to keep track of original image file location
image = Image.open("images/Default.png")#global variable to keep track of current image
stack = [] #global stack to keep track of all previous edits


def main():
    """Main method that initializes the GUI."""
    print("Hi")
    master = tk.Tk()#Initialize tkinter
    master.configure(bg='grey45') 

    startframe = tk.Frame(master)
    canvas = tk.Canvas(startframe, width=512, height=512) #Create intial window
    canvas.configure(bg='grey30')


    chooseFile(master, canvas) #grab starting file

    #Allows for re-choosing image
    chooseImageButton = tk.Button(master, text="Choose New Image", command=lambda: chooseFile(master, canvas))
    chooseImageButton.pack()

    #saves current image
    saveImageButton = tk.Button(master, text="Save Image", command=lambda: saveImage(image))
    saveImageButton.pack()

    startframe.pack()
    canvas.pack()

    #array of functions that create effects and filters of images
    Options = ["Invert Color", "Greyscale", "Black and White", "Color Scale", "Create Contour",
               "Add Contrast", "Increase Brightness", "Deep Fry",
               "Split Horizontally", "Split Vertically", "Fade Image"]
    variable = tk.StringVar(master)
    variable.set(Options[0])  # default value

    w = tk.OptionMenu(master, variable, *Options)
    w.pack() #packs all the options in the scrollbar

    confirmOptionsButton = tk.Button(master, text="Confirm", command=lambda: confirmButton(variable.get(),master, canvas))
    confirmOptionsButton.pack()#Creates the confirm button using the confirmButton() function

    resetImageButton = tk.Button(master, text="Reset", command=lambda: resetImage(master, canvas))
    resetImageButton.pack() #Creates the reset button using the resetImage() function

    revertImageButton = tk.Button(master, text="Undo", command=lambda: revertImage(master, canvas))
    revertImageButton.pack()#Creates the Undo button using the revertImage() function

    displayNewImage(startframe, canvas)

    master.mainloop()

def chooseFile(master, canvas):
    """Function that allows the user to navigate their directory for a photo."""
    global image, stack, file
    master.update()
    file = tk.filedialog.askopenfilename(initialdir="/", title="Select a File",
                                         filetypes=(("JPG files", ".jpg"), ("PNG files", ".png"),("JPEG files", ".jpeg")))
    # Selects a file
    
    if len(file) > 0: #checks to see if file is not null
        image = Image.open(file)
        image.convert("RGBA")
    #if()
    else:
        image = Image.open("images/Default.png")
        file = "images/Default.png"
        image.convert("RGBA")

    h, w = image.size
    if h == w or h > w: #if statement to help resize file to a maximum of (512,512)
        image = image.resize((512, int(512*w/h)))
    #if()
    else:
        image = image.resize((int(512*h/w), 512))
    #else()
    master.geometry(str(image.size[0] + 50) + "x" + str(image.size[1]+200))
    canvas.config(width=image.size[0], height=image.size[1]) #Configs the window around the image
    stack = [] #Do we really need this?
    master.update()
    displayNewImage(master, canvas)
#chooseFile()


def saveImage(image):
    """Function that saves the current image when called"""
    copy = image
    filename = filedialog.asksaveasfile(mode='w', defaultextension=".jpg")#makes a writable file
    if not filename:
        return
    #if()
    copy.save(filename)#saves the file
#saveImage()


def confirmButton(variable, master, canvas):
    """Function that receives signals from buttons and calls the matching method."""
    global stack, image, file
    copy = image
    originalImage = Image.open(file)
    h, w = originalImage.size
    if h == w or h > w:  # if statement to help resize file to a maximum of (512,512)
        originalImage = originalImage.resize((512, int(512 * w / h)))
    # if()
    else:
        originalImage = originalImage.resize((int(512 * h / w), 512))
    stack.append(image)
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
        root = tk.Toplevel()
        Options = ["red", "blue", "green"]#Options for Deepfry function
        variable = tk.StringVar(root)
        variable.set(Options[0])  # default value

        w = tk.OptionMenu(root, variable, *Options)#create pop up window
        w.pack()

        confirmOptionsButton = tk.Button(root, text="Confirm",
                                         command=lambda: deepFry(root, variable.get(), master, canvas))
        confirmOptionsButton.pack()#executes the function
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
        Options = ["chartreuse", "red", "blue", "green", "yellow", "cyan", "magenta"]  # Options for Deepfry function
        variable = tk.StringVar(root)
        variable.set(Options[0])  # default value

        w = tk.OptionMenu(root, variable, *Options)  # create pop up window
        w.pack()

        confirmOptionsButton = tk.Button(root, text="Confirm",
                                         command=lambda: colorScale(root, variable.get(), master, canvas))
        confirmOptionsButton.pack()  # executes the function
#confirmButton()


def displayNewImage(master, canvas):
    """Function that displays the newly edited image on the main window."""
    global image
    copy = image
    w,h = image.size
    one = ImageTk.PhotoImage(copy)
    master.one = one  # to prevent the image garbage collected.
    canvas.create_image((0, 0), image=one, anchor='nw')
#displayNewImage()


def deepFry(root, Domcolor, master, canvas):
    """Function that calls the imageMethods deepFry() function."""
    global image
    copy = image
    image = imgM.deepFry(copy, Domcolor)
    root.destroy()
    displayNewImage(master, canvas)
#deepFry()

def colorScale(root, color, master, canvas):
    global image
    copy = image
    if color == "chartreuse":
        image = imgM.colorscale(copy, chartreuse)
    #if()
    elif color == "red":
        image = imgM.colorscale(copy, red)
    # elif()
    elif color == "blue":
        image = imgM.colorscale(copy, blue)
    # elif()
    elif color == "green":
        image = imgM.colorscale(copy, green)
    # elif()
    elif color == "yellow":
        image = imgM.colorscale(copy, yellow)
    # elif()
    elif color == "cyan":
        image = imgM.colorscale(copy, cyan)
    #elif()
    elif color == "magenta":
        image = imgM.colorscale(copy, magenta)
    #elif()
    root.destroy()
    displayNewImage(master, canvas)


def resetImage(master, canvas):
    """Function that resets the image to it's original version."""
    global image, file
    image = Image.open(file)
    h, w = image.size
    if h == w or h > w:  # if statement to help resize file to a maximum of (512,512)
        image = image.resize((512, int(512 * w / h)))
    # if()
    else:
        image = image.resize((int(512 * h / w), 512))
    displayNewImage(master, canvas)
#resetImage()


def revertImage(master, canvas):
    """Function that sets the image back a previous edit."""
    global image, stack, file
    if len(stack) == 0: #check to see if stack is empty
        image = Image.open(file)
    else:
        latest = len(stack)-1
        image = stack[latest] #Set image to top of stack
        stack.remove(stack[latest])

    displayNewImage(master, canvas)
#revertImage()


if __name__ == "__main__":
    """Calls main function."""
    main()
