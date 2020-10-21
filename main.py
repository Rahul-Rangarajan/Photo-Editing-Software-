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
    
    testImage = Image.open("images/toocant.jpg").resize((512, 512))
    testImage = imgM.invertColor(testImage)
    testImage.show()





if __name__ == "__main__":
    main()
