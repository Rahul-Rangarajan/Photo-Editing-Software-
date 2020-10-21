'''
Contributors:
    Jack Castiglione
    Rahul Rangarajan
    Cameron King
    Nick Jonas
'''

import numpy as np
from PIL import Image

#Since this file while never be executed, there is no main() function.

#Invert the colors of an image
def invertColor(image):
    #Convert image to  array
    ar = np.asarray(image)

    #Make blank array with uint8 datatype
    #Default nparray datatype of f8 is unsupported by pillow
    newAr = np.empty((image.height, image.width, 3), np.uint8)

    #Invert all numbers in the array
    for x in range(image.height):
        for y in range(image.width):
            for z in range(3):
                newAr[x][y][z] = 255 - ar[x][y][z]

    #Convert new array to image and return
    new = Image.fromarray(newAr)
    return new
#invertColor

def imageMethod(image, otherParam="null"):
    #Do something
    x = 2 + 3

    #Return an Image
    return image
#imageMethod

    
