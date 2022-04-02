import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog
from colorsLib import colorDictionary
import imageMethods as imgM #Imports all functions needed

class imageEditor():
    file = "images/Default.png"
    image = Image.open("images/Default.png")
    undo = []
    redo = []
    contrastScale= float(1.0)
    contourScale=1.0
    brightnessScale=1.0

    def __init__(self):
        self.undo.clear()
        self.redo.clear()

        #skew each column *
    #__init__(self)


    def chooseImage(self, root, canvas):
        root.update()
        self.file = tk.filedialog.askopenfilename(initialdir="/", title="Select a File",
                                                  filetypes=(("JPG files", ".jpg"),
                                                             ("PNG files", ".png"),
                                                             ("JPEG files", ".jpeg")))
        # Selects a file

        if len(self.file) > 0:  # checks to see if file is not null
            self.image = Image.open(self.file)
            self.image.convert("RGBA")
        # if()
        else:
            self.image = Image.open("images/Default.png")
            self.file = "images/Default.png"
            self.image.convert("RGBA")
        # else

        self.undo.clear()  # clears the undo stack
        self.undo.append(self.image)  # adds the base image to the undo stack

        self.contrastScale = 1.0
        self.contourScale = 1.0
        self.brightnessScale = 1.0

        self.displayImage(root, canvas)
    #chooseImage(self, root, canvas)
    def displayImage(self, root, canvas):
        copy = Image.fromarray(np.asarray(self.image))
        h, w = copy.size
        if h == w or h > w:  # if statement to help resize file to a maximum of (512,512)
            copy = copy.resize((750, int(750 * w / h)))
        # if()
        else:
            copy = copy.resize((int(750 * h / w), 750))
        # else
        root.geometry(str(copy.size[0] + 50) + "x" + str(copy.size[1] + 200))
        canvas.config(width=copy.size[0], height=copy.size[1])  # Configs the window around the image
        root.update()

        one = ImageTk.PhotoImage(copy)
        root.one = one  # to prevent the image garbage collected.

        canvas.create_image((0, 0), image=one, anchor='nw')
    # displayNewImage()

    def saveImage(self):
        """Function that saves the current image when called.

            Parameters:
                    image (PIL.Image.Image) = The Image to be saved.
        """
        copy = Image.fromarray(np.asarray(self.image)).convert("RGBA")
        filename = filedialog.asksaveasfilename(defaultextension=".PNG")
        # makes a writable file
        if not filename:
            return
        # if
        elif filename.upper().endswith("JPG") or filename.upper().endswith("JPEG"):
            copy = copy.convert("RGB")
        copy.save(filename)  # saves the file
    # saveImage()

    def confirmButton(self, numVar, scale, root, canvas):
        """Function that receives signals from buttons and calls the matching method.

            Parameters:
                    variable (str) = A string that holds the chosen option.
                    master (tkinter.Tk) = An instance of tkinter.
                    canvas (tkinter.Canvas) = A tkinter window.

            Returns:
                    Nothing.
        """
        copy = Image.fromarray(np.asarray(self.image))
        originalImage = Image.open(self.file)
        self.undo.append(copy)
        self.redo.clear()
        # else()

        match numVar:
            case 1:
                self.image = imgM.invertColor(copy)
                self.displayImage(root, canvas)

            case 2:
                self.image = imgM.greyscale(copy)
                self.displayImage(root, canvas)

            case 3:
                self.image = imgM.blackNWhite(copy)
                self.displayImage(root, canvas)

            case 4:
                master = tk.Toplevel()
                Options = ["red", "blue", "green"]  # Options for Deepfry function
                variable = tk.StringVar(root)
                variable.set(Options[0])  # default value

                w = tk.OptionMenu(root, variable, *Options)  # create pop up window
                w.pack()

                confirmDeepFryButton = tk.Button(root, text="Okay",
                                                 command=lambda: self.deepFry(self, root, variable.get(), master, canvas))
                confirmDeepFryButton.pack()  # executes the function

            case 5:
                self.image = imgM.halfNHalfHorizontal(copy, originalImage)
                self.displayImage(root, canvas)

            case 6:
                self.image = imgM.halfNHalfVertical(copy, originalImage)
                self.displayImage(root, canvas)

            case 7:
                self.image = imgM.fadeFilter(copy, originalImage)
                self.displayImage(root, canvas)

            case 8:
                master = tk.Toplevel()
                Options = ["Red", "Blue", "Green", "Yellow",
                        "Chartreuse", "Cyan", "Magenta",
                        "Transparent"]  # Options for Colorscale function

                variable = tk.StringVar(root)
                variable.set(Options[0])  # default value

                w = tk.OptionMenu(root, variable, *Options)  # create pop up window
                w.pack()

                confirmOptionsButton = tk.Button(root, text="Confirm",
                                                 command=lambda: self.colorScale(self, root, variable.get(), master, canvas))
                confirmOptionsButton.pack()  # executes the function
            case 9:
                scaleN = self.scaler(self.contrastScale, scale)
                self.contrastScale=scale
                self.image= imgM.addContrast(copy, scaleN)
                self.displayImage(root, canvas)
            case 10:
                scaleN = self.scaler(self.brightnessScale, scale)
                self.brightnessScale = scale
                self.image = imgM.addBrightness(copy, scaleN)
                self.displayImage(root, canvas)
            case 11:
                scaleN = self.scaler(self.contourScale, scale)
                self.contourScale = scale
                self.image = imgM.createContour(copy, scaleN)
                self.displayImage(root, canvas)
        #match
    # confirmButton()
    def scaler(self, scaleO, scaleN):
        if scaleN == 0.0:
            scaleN -= scaleO
        else:
            scaleN = 100/float(scaleN)
            scaleN -= scaleO
        return scaleN
    #scaler
    def deepFry(self, root, Domcolor, master, canvas):
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
        self.displayImage(master, canvas)
    # deepFry()
    def colorScale(self, root, color, master, canvas):
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
        # if()
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
        # elif()
        elif color == "Magenta":
            image = imgM.colorscale(copy, colorDictionary["Magenta"])
        # elif()
        elif color == "Transparent":
            image = imgM.colorscale(copy, colorDictionary["Transparent"])
            print("What did you expect?")
        # elif()

        root.destroy()
        self.displayImage(master, canvas)
    # colorScale()

    def resetImage(self, root, canvas):
        """Function that resets the image to it's original version.

            Parameters:
                    root (tkinter.Tk) = An instance of tkinter.
                    canvas (tkinter.Canvas) = A tkinter window.
        """

        self.undo.append(self.image)  # add the original image to the stack
        image = self.undo[0]  # set the original image as the current image

        self.displayImage(root, canvas)
        # else()
    # resetImage()


