import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
import imageMethods as imgM #Imports all functions needed

class imageEditor():
    file = "images/Default.png"
    image = Image.open("images/Default.png")
    undo = []
    redo = []
    scaleStack = []
    stackSelect = False
    contrastScale= float(1.0)
    contourScale=1.0
    brightnessScale=1.0

    def __init__(self):
        self.undo.clear()
        self.redo.clear()
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
        if self.stackSelect == True:
            self.scaleStack.append(copy)
        else:
            self.undo.append(copy)
        self.redo.clear()
        print(scale)


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
                match scale:
                    case 'red':
                        self.image = imgM.deepFry(copy, 'red')
                    case 'blue':
                        self.image = imgM.deepFry(copy, 'blue')
                    case 'green':
                        self.image = imgM.deepFry(copy, 'green')
                #match
                self.displayImage(root, canvas)
            case 5:
                match scale:
                    case 'Half&Half Horizontal':
                        self.image = imgM.halfNHalfHorizontal(copy, originalImage)
                        self.displayImage(root, canvas)
                    case "Half&Half Vertical":
                        self.image = imgM.halfNHalfVertical(copy, originalImage)
                        self.displayImage(root, canvas)

            case 7:
                self.image = imgM.fadeFilter(copy, originalImage)
                self.displayImage(root, canvas)

            case 8:
                color_code = colorchooser.askcolor(title="Choose color")[0]
                color_code = color_code+(255,)
                self.image = imgM.colorscale(self.image, color_code)
                self.displayImage(root, canvas)

            case 9:
                scaleN = self.scaler(self.contrastScale, scale)
                self.contrastScale = scale
                self.image = imgM.addContrast(copy, scaleN)
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
        if numVar < 9 and self.stackSelect == True:
            self.undo.append(self.scaleStack)
            self.stackSelect = False
        elif numVar >= 9 and self.stackSelect == False:
            self.stackSelect = True

    # confirmButton()

    def scaler(self, scaleO, scaleN):
        if scaleN == 0.0:
            scaleN -= scaleO
        else:
            scaleN = 100/float(scaleN)
            scaleN -= scaleO
        return scaleN
    #scaler
    def deepFry(self, root, Domcolor, canvas):
        """Function that calls the imageMethods deepFry() function.

            Parameters:
                    root (tkinter.Toplevel) = A pop up window.
                    Domcolor (str) = The selected option for the imgM.deepFry function
                    master (tkinter.Tk) = An instance of tkinter.
                    canvas (tkinter.Canvas) = A tkinter window.
        """
        copy = Image.fromarray(np.asarray(self.image))
        self.image = imgM.deepFry(copy, Domcolor)
        self.displayImage(root, canvas)
    # deepFry()

    def resetImage(self, root, canvas):
        """Function that resets the image to its original version.

            Parameters:
                    root (tkinter.Tk) = An instance of tkinter.
                    canvas (tkinter.Canvas) = A tkinter window.
        """

        self.undo.append(self.image)  # add the original image to the stack
        self.image = self.undo[0]  # set the original image as the current image

        self.displayImage(root, canvas)
        # else()
    # resetImage()

    def revertImage(self, master, canvas):
        """Function that is ctrl+ y to undo's ctrl+z.

                Parameters:
                        master (tkinter.Tk) = An instance of tkinter.
                        canvas (tkinter.Canvas) = A tkinter window.
        """
        if len(self.redo) != 0:
            self.undo.append(self.image)
            self.image = self.redo.pop()  # Set image to top of undo stack
        #if()
        self.displayImage(master, canvas)
    #revertImage()

    def undoImage(self,master, canvas):
        """Function that sets the image back a previous edit.

            Parameters:
                    master (tkinter.Tk) = An instance of tkinter.
                    canvas (tkinter.Canvas) = A tkinter window.
        """
        if len(self.undo) == 1:  # check to see if undo stack is empty
            self.image = self.undo[0]
        # if()
        else:
            self.redo.append(self.image)
            self.image = self.undo.pop()  # Set image to top of undo stack

        # else()
        self.displayImage(master, canvas)
    # undoImage()

