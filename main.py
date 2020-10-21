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
import os
import imageMethods as imgM


def main():
    print("Hi")
    image = Image.open("images/Leia.jpg")
    #Where the image should be saved, by default is the same directory
    #that this file is in
    path, filename = os.path.split(os.path.abspath(__file__))
    print(filename)
    
    
    #testImage = Image.open("images/toocant.jpg").resize((512, 512))
    #testImage = imgM.invertColor(testImage)
    #testImage.show()





if __name__ == "__main__":
    main()
