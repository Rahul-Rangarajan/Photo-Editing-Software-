'''
Contributors:
    Jack Castiglione
    Rahul Rangarajan
    Cameron King
    Nick Jonas
'''

import numpy as np
import time
from PIL import Image, ImageFilter, ImageEnhance

#Since this file while never be "executed", there is no main() function.

def invertColor(image):
    """Invert the colors of an image.

        Parameters:
                image (PIL.Image.Image) = The image to be modified.
        Returns:
                new (PIL.Image.Image) = The modified image
    """
    #Convert image to  array
    ar = np.asarray(image.convert("RGBA"))

    #Invert all numbers in the array except for transparency value
    newAr = np.array(abs((255, 255, 255, 0) - ar), np.uint8)

    #Convert new array to image and return
    new = Image.fromarray(newAr)
    return new
#invertColor()


def greyscale(image):
    """Convert image to greyscale.

        Parameters:
                image (PIL.Image.Image) = The image to be modified.
        Returns:
                greyImage (PIL.Image.Image) = The modified image.
    """
    #Convert image to array
    ar = np.asarray(image.convert("RGBA"))

    #Separate array into parts
    color = np.asarray(ar.dot([1/3, 1/3, 1/3, 0]), np.uint8)
    alpha = np.asarray(ar.dot([0,0,0,1]), np.uint8)

    #Recombine parts and return
    out = np.asarray(np.asarray([color.T, color.T, color.T, alpha.T]).T, np.uint8)
    return Image.fromarray(out)
#greyscale()



def blackNWhite(image):
    """Converts an image to pure black and white.

        Parameters:
                image (PIL.Image.Image) = The image to be modified.
        Returns:
                black_n_white (PIL.Image.Image) = The modified image.
    """
    #Convert image to array
    ar = np.asarray(image.convert("RGBA"))

    #Separate array into parts
    color = np.asarray(ar.dot([1/3, 1/3, 1/3, 0]), np.uint8)
    alpha = np.asarray(ar.dot([0,0,0,1]), np.uint8)

    #Modify color array to set values
    color[color >= 128] = 255
    color[color < 128] = 0

    #Recombine parts and return
    out = np.asarray(np.asarray([color.T, color.T, color.T, alpha.T]).T, np.uint8)
    return Image.fromarray(out)
#blackNWhite()


def createContour(image):
    """Apply Contour to an image.

        Parameters:
                image (PIL.Image.Image) = The image to be modified.
        Returns:
                imageFinal (PIL.Image.Image) = The modified image.
    """
    #Apply Contour filter
    imageContour = image.copy()
    imageContour= imageContour.filter(ImageFilter.CONTOUR)

    #Take out some of the color
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(0.3)  

    #Blend the images together
    imageFinal = Image.blend(image, imageContour, 0.4)  
    return imageFinal
#createContour()


def addContrast(image):
    """Adds contrast to an image.

        Parameters:
                image (PIL.Image.Image) = The image to be modified.
        Returns:
                contrast.enhance(1.75) (PIL.Image.Image) = The modified Image.
    """
    #Use the pillow contrast method to add contrast
    contrast = ImageEnhance.Contrast(image)
    return contrast.enhance(1.75)
#addContrast()


def addBrightness(image):
    """Adds Brightness to an image.

        Parameters:
                image (PIL.Image.Image) = The image to be modified.
        Returns:
                bright.enhance(1.1) = The modified image.
    """
    #Use the pillow brightness method to add brightness
    bright = ImageEnhance.Brightness(image)
    return bright.enhance(1.1)
#addBrightness()



def deepFry(image, Domcolor):
    """Deepfrys an input image.

    Takes a specified rgb name and increases it in
    all instances of the picture. Also decreases a
    non specified rgb value so the photo doesn't become
    completely white.

        Parameters:
                image (PIL.Image.Image) = The image to be modified.
                Domcolor (str) = The user choice for deciding which color
                to deepfry with.
        Returns:
                bright.enhance(3.0) (PIL.Image.Image) = The modified Image.
    """
    Domcolor = Domcolor.lower()
    imageAr = np.asarray(image.convert("RGBA"))
    
    if Domcolor == "red":
        newAr = imageAr + [+50, -50, 0, 0]
        newAr[newAr > 255] = 255
        newAr[newAr < 0] = 0
        newAr = np.array(newAr, np.uint8)
        image=Image.fromarray(newAr)
    #if()
    
    elif Domcolor == "blue":
        newAr = imageAr + [-50, 0, +50, 0]
        newAr[newAr > 255] = 255
        newAr[newAr < 0] = 0
        newAr = np.array(newAr, np.uint8)
        image=Image.fromarray(newAr)
    #elif()
    
    elif Domcolor == "green":
        newAr = imageAr + [0, +50, -50, 0]
        newAr[newAr > 255] = 255
        newAr[newAr < 0] = 0
        newAr = np.array(newAr, np.uint8)
        image=Image.fromarray(newAr)
    #elif()
    
    contrast = ImageEnhance.Contrast(image)
    imageCon = contrast.enhance(3.0)
    # upping the contrast to create distinction between colors
    bright = ImageEnhance.Brightness(imageCon)
    # upping the brightness to emphasize the bighter colors
    return bright.enhance(3.0)
#deepFry()


def halfNHalfHorizontal(image1, image2):
    """Function that creates a half-n-half image.
    
    The image is composed of one half of image1 and one
    half of image2. The images are divided on an invisible
    horizontal line in the center of the picture.

        Parameters:
            image1 (PIL.Image.Image) = One of the images to be combined
            image2 (PIL.Image.Image) = One of the images to be combined
        Returns:
            Image.fromarray(newAr) (PIL.Image.Image) = The combined images.
    """
    # Convert both images to RGBA
    image1 = image1.convert("RGBA")
    image2 = image2.convert("RGBA")

    # Determine the size of the image
    h1, w1 = image1.size

    # Create arrays for each image
    image1Array = np.asarray(image1)
    image2Array = np.asarray(image2)

    # Create an empty array with the same dimensions
    newAr = np.empty((w1, h1, 4), np.uint8)

    # Set each pixel in the new array to the pixel from the proper image
    for i in range(w1):
        for j in range(h1):
            if i < w1 // 2:
                newAr[i][j] = image1Array[i][j]
            #if()
            else:
                newAr[i][j] = image2Array[i][j]
            #else()
        # for
    # for

    # Return an image created from the new array
    return Image.fromarray(newAr)
#halfNHalfHorizontal()


def halfNHalfVertical(image1, image2):
    """Function that creates a half-n-half image.
    
    The image is composed of half of image1 and
    half of image2. The images are divided by an
    invisible vertical line in the center of the
    picture.

        Parameters:
            image1 (PIL.Image.Image) = One of the images to be combined
            image2 (PIL.Image.Image) = One of the images to be combined
        Returns:
            Image.fromarray(newAr) (PIL.Image.Image) = The combined images.

    """
    #Convert both images to RGBA
    image1 = image1.convert("RGBA")
    image2 = image2.convert("RGBA")

    #Determine the size of the image
    h1, w1 = image1.size

    #Create arrays for each image
    image1Array = np.asarray(image1)
    image2Array = np.asarray(image2)

    #Create an empty array with the same dimensions
    newAr = np.empty((w1, h1, 4), np.uint8)

    #Set each pixel in the new array to the pixel from the proper image
    for i in range(w1):
        for j in range(h1):
            if j < h1 // 2:
                newAr[i][j] = image1Array[i][j]
            #if()
            else:
                newAr[i][j] = image2Array[i][j]
            #else()
        #for
    #for

    #Return an image created from the new array
    return Image.fromarray(newAr)
#halfNHalfVertical


def colorscale(image, color):
    """Function that scales and image's color based on color input.

        This function takes an input color and
        scales all color in a picture based off
        of this color, almost as if it were a
        greyscale photo but with a different color
        of choice.

        Parameters:
                image (PIL.Image.Image) = The image to be modified.
                color (tuple) = A tuple of ints that represent an
                rgba value.
        Returns:
                Image.fromarray(final) (PIL.Image.Image) = The modified image.
    """
    #Save image size
    imageArray = np.asarray(image.convert("RGBA"))

    #Perform an operation for each pixel in the image
    out = np.asarray(imageArray * color / 255, np.uint8)
    
    print(type(color))

    return Image.fromarray(out)
#colorscale()


def fadeFilter(imgOne, imgTwo):
    """Function that uses a premade image to create a fade effect.

        Fades over two different images using a mask created from
        a premade filter.

        Parameters:
                imgOne (PIL.Image.Image) = One of the images to be combined.
                imgTwo (PIL.Image.Image) = One of the images to be combined.
        Returns:
                img (PIL.Image.Image) = The combined images.
    """
    imgOneW, imgOneH = imgOne.size
    fade = Image.open("images/FadeFilter.jpg").convert("L")
    #Grab custom mask
    fade = fade.resize((imgOneW, imgOneH), Image.NEAREST)
    img = Image.composite(imgOne, imgTwo, fade)
    #Use mask to create a blend/fade
    return img
#fadeFilter()
