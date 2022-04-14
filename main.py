'''
Contributors:
    Jack Castiglione
    Rahul Rangarajan
    Cameron King
    Nick Jonas
'''
#colorchooser
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from colorsLib import colorDictionary
import imageMethods as imgM #Imports all functions needed
from imageEditor import imageEditor

file = "images/Default.png"#global variable to keep track of original image file location
image = Image.open("images/Default.png")#global variable to keep track of current image
undo = [] #global stack to keep track of all previous edits
redo = []#global stack to keep track of all previous undo


def main():
    root = tk.Tk()  # Initialize tkinter)
    # setting tkinter window size
    #root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

    canvas = tk.Canvas(root, width=750, height=750)
    root.configure(bg='grey45')
    canvas.configure(bg='grey30')
    canvas.pack(side='left')
    control = imageEditor()
    control.chooseImage(root, canvas)

    #choose button
    chooseImageButton = tk.Button(root, text="Choose New Image",
                                  command=lambda: control.chooseImage(root, canvas))
    chooseImageButton.pack()

    #save button
    saveImageButton = tk.Button(root, text="Save Image",
                                command=lambda: control.saveImage())
    saveImageButton.pack()

    # reset button
    resetButton = tk.Button(root, text='Reset',
                            command=lambda: resetImage(control, root, canvas, contrastSlider, contourSlider,
                                                       brightnessSlider))
    resetButton.place(x=1125, y=53)

    # revert
    revertButton = tk.Button(root, text='Revert', command=lambda:control.revertImage(root, canvas))
    revertButton.place(x=1100, y=80)

    # undo
    undoButton = tk.Button(root, text='Undo  ', command=lambda: control.undoImage(root, canvas))
    undoButton.place(x=1145, y=80)

    #contrast Slider
    contrastSlider = tk.Scale(root, from_=100, label = 'Contrast', to=-100,
                                    command=lambda x:control.confirmButton(9, float(x), root, canvas),
                                    showvalue=0)
    contrastSlider.place(x = 1105, y = 110)

    #contour Slider
    contourSlider = tk.Scale(root, from_=100, label = 'Contour', to=-100,
                                    command=lambda x:control.confirmButton(11, float(x), root, canvas),
                                    showvalue=0)
    contourSlider.place(x = 1000, y = 110)

    #brightness Slider
    brightnessSlider = tk.Scale(root, from_=100, label='Brightness', to=-100,
                             command=lambda x: control.confirmButton(10, float(x), root, canvas),
                             showvalue=0)
    brightnessSlider.place(x = 1210, y = 110)

    #invert color
    invertColor = tk.Button(root, text='Invert Color',
                            command=lambda: control.confirmButton(1, 0, root, canvas ))
    invertColor.place(x=1000, y=400)

    #greyscale
    greyScale = tk.Button(root, text='Greyscale',
                            command=lambda: control.confirmButton(2, 0, root, canvas))
    greyScale.place(x=1100, y=400)

    #black and white
    blackNWhite = tk.Button(root, text='Black&White',
                          command=lambda: control.confirmButton(3, 0, root, canvas))
    blackNWhite.place(x=1200, y=400)

    # fade
    fade = tk.Button(root, text='Fade Filter',
                            command=lambda: control.confirmButton(7, 0, root, canvas))
    fade.place(x=1000, y=450)

    # fade
    colorScale = tk.Button(root, text='Colorscale',
                     command=lambda: control.confirmButton(8, 0, root, canvas))
    colorScale.place(x=1100, y=450)

    #deepfry
    Options = ["red", "green", "blue"]  # Options for deepfry
    variable = tk.StringVar(root, )
    variable.set(Options[0])
    w = tk.OptionMenu(root, variable, *Options,
                      command=lambda x:control.confirmButton(4, x, root, canvas)) # create pop up window
    w.place(x=1000, y=600)

    #Half and Half Vertical and Horizontal
    Options = ["Half&Half Horizontal", "Half&Half Vertical"]  # Options for Half & Half functions
    variable = tk.StringVar(root, )
    variable.set(Options[0])
    w = tk.OptionMenu(root, variable, *Options, command=lambda x:control.confirmButton(5, x, root, canvas) )  # create pop up window
    w.place(x=1000, y=700)


    root.mainloop()



#main()
def resetImage(control, root, canvas, contrastSlider, contourSlider, brightnessSlider):
    """Function that resets the image to it's original version.

        Parameters:
                master (tkinter.Tk) = An instance of tkinter.
                canvas (tkinter.Canvas) = A tkinter window.
    """
    contrastSlider.set(0)
    print(contrastSlider.get())
    contourSlider.set(0)
    brightnessSlider.set(0)
    control.resetImage(root, canvas)
#resetImage()

if __name__ == "__main__":
    """Calls main function."""
    main()
