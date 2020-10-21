'''
Contributors:
    Jack Castiglione
    Rahul Rangarajan
    Cameron King
    Nick Jonas
'''

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

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
#invertColor()

def greyscale(image):
    #Convert image to greyscale
    greyImage = image.convert("L")

    #Convert back to RGBA
    greyImage = image.convert("RGBA")

    #returns greyscaled image
    return greyImage
#greyscale()

def blackNWhite(image):

    #Convert image to grey
    grayC = image.convert("L")

    #Convert image to array that is not read only
    arrayC = np.asarray(grayC).copy()

    arrayC[arrayC < 128] = 0  # black
    arrayC[arrayC > 128] = 255  # white

    #Convert array back to image and returns
    black_n_white_cosmo = Image.fromarray(arrayC)
    return black_n_white_cosmo
#blackNWhite()

def createContour(image):
    imageContour = image.copy()
    imageContour= imageContour.filter(ImageFilter.CONTOUR)  # Apply Contour filter

    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(0.3)  # take out some of the color

    imageFinal = Image.blend(image, imageContour, 0.4)  # blend the images together
    return imageFinal
#createContour()


#Do Something
def imageMethod(image, otherParam="null"):
    #Do something
    x = 2 + 3

    #Return an Image
    return image
#imageMethod

    
