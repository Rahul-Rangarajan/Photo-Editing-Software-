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
    greyImage = greyImage.convert("RGBA")

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

def createContrast(image):
    contrast = ImageEnhance.Contrast(image)
    return contrast.enhance(7.0)
#createContrast()

def createBrightness(image):
    bright = ImageEnhance.Brightness(image)
    return bright.enhance(3.0)
#createBrightness()

def deepFry(image):
    imageW, imageH = image.size
    for i in range(imageW):  # width
        for j in range(imageH):  # height
            pixel = image.getpixel((i, j))
            # print(pixel)
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            if g >= 50:  # reducing green beyond a point
                g = g - 50
            if r <= 205:  # increasing red below a point
                r = r + 50
            newColor = (r, g, 0)  # modifying the pixel rgb values
            image.putpixel((i, j), newColor)  # Places in new rgb values

    contrast = ImageEnhance.Contrast(image)
    imageCon = contrast.enhance(3.0)
    # upping the contrast to create distinction between colors

    bright = ImageEnhance.Brightness(imageCon)
    return bright.enhance(3.0)
    # upping the brightness to emphasize the bighter colors
#deepFry()

def halfNHalfHorizontal(image1, image2):
    image1 = image1.convert("RGBA")
    image2 = image2.convert("RGBA")

    h, w = image1.size

    image1Array = np.asarray(image1)
    image2Array = np.asarray(image2)

    size = image1Array.shape
    newAr = np.empty((h, w, 4), np.uint8)

    image2.show()

    for i in range(size[0]):
        for j in range(size[1]):
            if i < size[0] // 2:
                newAr[i][j] = image1Array[i][j]
            else:
                newAr[i][j] = image2Array[i][j]
    #for

    return Image.fromarray(newAr)
#halfNHalfHorizontal()

def halfNHalfVertical(image1, image2):
    image1 = image1.convert("RGBA")
    image2 = image2.convert("RGBA")

    h1, w1 = image1.size
    h2, w2 = image2.size

    image1Array = np.asarray(image1)
    image2Array = np.asarray(image2)

    newAr = np.empty((w1, h1, 4), np.uint8)

    for i in range(w1):
        for j in range(h1):
            if j < h1 // 2:
                newAr[i][j] = image1Array[i][j]
            else:
                newAr[i][j] = image2Array[i][j]
    # for

    return Image.fromarray(newAr)
#halfNHalfVertical

#Do Something
def imageMethod(image, otherParam="null"):
    #Do something
    x = 2 + 3

    #Return an Image
    return image
#imageMethod

    
