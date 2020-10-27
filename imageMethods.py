'''
Contributors:
    Jack Castiglione
    Rahul Rangarajan
    Cameron King
    Nick Jonas
'''

import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

#Since this file while never be "executed", there is no main() function.

def invertColor(image):
    """Invert the colors of an image.

        Parameters:
                image (PIL.Image.Image) = The image to be modified.
        Returns:
                new (PIL.Image.Image) = The modified image
    """
    ar = np.asarray(image)#Convert image to  array

    #Make blank array with uint8 datatype
    #Default nparray datatype of f8 is unsupported by pillow
    newAr = np.empty((image.height, image.width, 3), np.uint8)

    #Invert all numbers in the array
    for x in range(image.height):
        for y in range(image.width):
            for z in range(3):
                newAr[x][y][z] = 255 - ar[x][y][z]
            #for
        #for
    #for

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
    greyImage = image.convert("L")

    #Convert back to RGBA
    greyImage = greyImage.convert("RGBA")

    #returns greyscaled image
    return greyImage
#greyscale()



def blackNWhite(image):
    """Converts an image to pure black and white.

        Parameters:
                image (PIL.Image.Image) = The image to be modified.
        Returns:
                black_n_white (PIL.Image.Image) = The modified image.
    """
    #Convert image to grey
    grayC = image.convert("L")

    #Convert image to array that is not read only
    arrayC = np.asarray(grayC).copy()

    #Set colors below 128 to black and other values to white
    arrayC[arrayC <= 128] = 0  # black
    arrayC[arrayC >= 128] = 255  # white

    #Convert array back to image and returns
    black_n_white = Image.fromarray(arrayC)
    # Convert image to RGBA
    black_n_white = black_n_white.convert("RGBA")
    return black_n_white
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
    imageW, imageH = image.size
    Domcolor = Domcolor.lower()
    if Domcolor == "red":
        for i in range(imageW):  # width
            for j in range(imageH):  # height
                pixel = image.getpixel((i, j))
                # print(pixel)
                r = pixel[0]
                g = pixel[1]
                if g >= 50:  # reducing green beyond a point
                    g = g - 50
                if r <= 205:  # increasing red below a point
                    r = r + 50
                newColor = (r, g, 0)  # modifying the pixel rgb values
                image.putpixel((i, j), newColor)  # Places in new rgb values
            #for
        #for
    #if()
    
    elif Domcolor == "blue":
        for i in range(imageW):  # width
            for j in range(imageH):  # height
                pixel = image.getpixel((i, j))
                # print(pixel)
                r = pixel[0]
                b = pixel[2]
                if r >= 50:  # reducing green beyond a point
                    r = r - 50
                if b <= 205:  # increasing red below a point
                    b = b + 50
                newColor = (r, 0, b)  # modifying the pixel rgb values
                image.putpixel((i, j), newColor)  # Places in new rgb values
            #for
        #for
    #elif()
    
    elif Domcolor == "green":
        for i in range(imageW):  # width
            for j in range(imageH):  # height
                pixel = image.getpixel((i, j))
                # print(pixel)
                g = pixel[1]
                b = pixel[2]
                if b >= 50:  # reducing green beyond a point
                    b = b - 50
                if g <= 205:  # increasing red below a point
                    g = g + 50
                newColor = (0, g, b)  # modifying the pixel rgb values
                image.putpixel((i, j), newColor)  # Places in new rgb values
            #for
        #for
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
    imageArray = np.asarray(image)
    height = imageArray.shape[0]
    width = imageArray.shape[1]

    #Create final location
    final = np.ndarray(shape=(height, width, 4), dtype=np.uint8)

    #Perform an operation for each pixel in the image
    for i in range(height):
        for j in range(width):
            #Create an RGB value from the color and grey level
            for k in range(3):
                final[i][j][k] = (imageArray[i][j][k] / 256 * color[k])
            #Insert alpha value
            final[i][j][3] = color[3]
            #for
        #for
    #for

    return Image.fromarray(final)
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
