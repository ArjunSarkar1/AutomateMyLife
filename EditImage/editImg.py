from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import os
import cv2

# Input Images Dir
pathIn = os.path.join(os.getcwd(), "inputImgs")

# Edited Images Dir
pathOut = os.path.join(os.getcwd(), "editedImgs")

'''
///////////
editBatch//
///////////

The function `editBatch` processes image files in a specified input directory and applies a vintage
edit before saving the edited images to an output directory.

:param pathIn: The `pathIn` parameter in the `editBatch` function is the directory path where the
input images are located. These images will be processed by the `vintageEdit` function
:param pathOut: The `pathOut` parameter in the `editBatch` function is the directory path where the
edited images will be saved after processing
'''
def editBatch(pathIn,pathOut,t):
    checkDirectory(pathOut)
    
    for filename in os.listdir(pathIn):
        if filename.endswith((".jpg", ".png")):
            inputPath = os.path.join(pathIn, filename)
            outputPath = os.path.join(pathOut, filename)
            selectEdit(inputPath,outputPath,t)
            print(f"Edited image saved to {pathOut}")

def cinematicEdit(pathIn,pathOut):
    #--------------------------------------#
    img = Image.open(pathIn).convert("RGB")
    #--------------------------------------#
    r, g, b = img.split()
    r = adjustChannel(r, 1.1)
    g = adjustChannel(g, 1.01)
    b = adjustChannel(b, 0.9)
    img = Image.merge("RGB", (r, g, b))
    #--------------------------------------# 
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.3) 
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)
    #--------------------------------------# 
    img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
    #--------------------------------------# 
    np_img = np.array(img)
    rows, cols = np_img.shape[:2]
    kernel_x = cv2.getGaussianKernel(cols, cols // 3)
    kernel_y = cv2.getGaussianKernel(rows, rows // 3)
    kernel = kernel_y * kernel_x.T
    vignette = 255 * kernel / np.linalg.norm(kernel)
    vignette = np.dstack((vignette, vignette, vignette))
    np_img = cv2.addWeighted(np_img, 0.8, vignette.astype(np.uint8), 0.2, 0)
    img = Image.fromarray(np.clip(np_img, 0, 255).astype(np.uint8))
    #--------------------------------------# 
    img = ImageOps.expand(img, border=(0, img.height // 6), fill="black")
    #--------------------------------------# 
    img.save(pathOut)

"""
///////////////
Vintage Edit //
///////////////

Purpose:
Applies a "vintage" effect to an image by manipulating its color channels, 
adding noise, adjusting brightness and contrast, and overlaying a vignette filter.
The processed image is then saved to a specified output path.

Explanation:
- Input Image Conversion: The function begins by opening the input image file and 
converting it to the RGB color mode.

- Color Adjustment: The red, green, and blue channels are individually 
adjusted to enhance red tones, slightly increase green, and reduce blue for a warmer effect.

- Blurring: A Gaussian blur is applied to soften the image slightly.

- Noise Addition: Random noise is introduced to simulate an aged or
"vintage" texture, with pixel values clipped to valid ranges.

- Brightness & Contrast Enhancement: The brightness is increased by 10%, 
and the contrast by 20% for more vivid colors.

- Vignette Effect: A Gaussian kernel is used to generate a vignette mask, 
which darkens the image edges for a classic look.

- Save Processed Image: The final processed image is saved to the specified
output path, and the file path is printed for confirmation.
"""
def vintageEdit(pathIn,pathOut):
    #--------------------------------------#
    img = Image.open(pathIn).convert("RGB")
    #--------------------------------------#
    r, g, b = img.split()
    r = adjustChannel(r, 1.2)
    g = adjustChannel(g, 1.1)
    b = adjustChannel(b, 0.9)
    img = Image.merge("RGB", (r, g, b))
    #--------------------------------------#
    img = img.filter(ImageFilter.GaussianBlur(0.3))
    #--------------------------------------#
    np_img = np.array(img)
    noise = np.random.normal(0, 3, np_img.shape) 
    np_img = np.clip(np_img + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(np_img)
    #--------------------------------------#
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.05) 
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)
    #--------------------------------------#
    rows, cols = np_img.shape[:2]
    kernel_x = cv2.getGaussianKernel(cols, cols // 5)
    kernel_y = cv2.getGaussianKernel(rows, rows // 5)
    kernel = kernel_y * kernel_x.T
    mask = 180 * kernel / np.linalg.norm(kernel)
    vignette = np.dstack((mask, mask, mask))
    np_img = cv2.addWeighted(np_img, 0.7, vignette.astype(np.uint8), 0.35, 0)
    img = Image.fromarray(np_img)
    img = img.filter(ImageFilter.UnsharpMask(radius=3, percent=150, threshold=3))
    #----------------------------------------#
    img.save(pathOut)

'''
///////////////
Drawing Edit //
///////////////

Purpose:
- This function transforms input images into hand-drawn, pencil-sketch-like pictures, using a series of image-processing steps. It creates a unique, artistic effect that highlights key features and emphasizes lines, mimicking the look of a hand-drawn sketch.

Explanation:
- First, we convert the image to grayscale.
This removes the colors and turns the image into black and white. 
By doing this, we give the image the appearance of a pencil sketch, 
where light and shadow are represented in varying shades of gray.

- Next, we apply a Gaussian blur. This step softens the details of the image, creating a smoother, more artistic effect. The blur helps remove 
some of the harsh lines and sharp details that you wouldn't typically find in a hand-drawn sketch.

- Then, we enhance the contrast and adjust the brightness. 
We increase the contrast to make the key features in the image stand out more, 
giving it more depth and definition. We also slightly decrease the brightness to 
add some shadow and create a more authentic sketch-like mood.

- After that, we apply edge detection: Using a technique called 
Canny edge detection (via OpenCV), we highlight the main lines and contours
of the image. This step helps us define the edges, giving the image the
characteristic outline of a pencil drawing.

- We then invert the edges. By inverting the edges, the lines turn 
from black to white, and the background becomes black. This mimics the classic 
look of pencil sketches, where dark outlines stand out against a lighter background.

- Next, we blend the original image with the edge-detected image. This step combines the softened grayscale image with the highlighted edges. By blending them together, we create the final "hand-drawn" effect, where the sharp edges overlay the soft tones of the original image.

- Lastly, we apply sharpening: To make the lines more defined and emphasize the edges even further, we apply a sharpening filter. This gives the sketch its final polished look, with crisp and clear lines that stand out.
'''
def drawingEdit(pathIn,pathOut):
    try:
        with Image.open(pathIn) as img:
            img = img.convert("L")
            img = img.filter(ImageFilter.GaussianBlur(radius=0.55))
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.95)
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.80)
            img_cv = np.array(img)
            edges = cv2.Canny(img_cv, 100, 200)
            edges_img = Image.fromarray(edges)
            edges_img = ImageOps.invert(edges_img)
            img = Image.blend(img.convert("RGB"), edges_img.convert("RGB"), alpha=0.4)

            for _ in range(2):
                img = img.filter(ImageFilter.SHARPEN)

            img.save(pathOut)
                #-----------------------------------------#
    except:
        print(f"Error processing {pathIn}")
 
def selectEdit(inputPath,outputPath,t):
    if t == 'c':
        cinematicEdit(inputPath,outputPath)
    elif t == 'v':
        vintageEdit(inputPath,outputPath)
    elif t == 'd':
        drawingEdit(inputPath,outputPath)

"""
The function `adjustChannel` takes an image channel and a factor, multiplies each pixel value by
the factor, and returns the adjusted channel.

:param channel: The `channel` parameter in the `adjust_channel` function likely refers to an image
channel, such as the red, green, or blue channel of an image. In image processing, an image is
typically composed of multiple channels, each representing different color information

:param factor: The `factor` parameter in the `adjust_channel` function represents the value by which
each pixel in the channel will be multiplied to adjust its intensity or brightness. This factor can
be used to make the channel brighter (if factor > 1), darker (if 0 < factor < 1),

:return: The function `adjustChannel` is returning an adjusted channel with the pixel values
multiplied by the factor provided as an argument.
"""
def adjustChannel(channel, factor):
    adjusted_pixels = []
    for pixel in channel.getdata():
        prod = int(pixel * factor)
        adjusted_pixels.append(prod)
    adjusted_channel = channel.copy()
    adjusted_channel.putdata(adjusted_pixels)
    return adjusted_channel

'''
This function takes two parameters: pathIn and pathOut.
- pathIn is the path to the directory containing the images to be edited.
- pathOut is the path to the directory where the edited images will be saved.
'''
def checkDirectory(pathOut):
    if not os.path.exists(pathOut):
        os.makedirs(pathOut)

def startEditing():
    print("""
    ****************************************
    *        Welcome to Image Editor       *
    ****************************************
    """)
    input("Press Enter to start the image editing process...\n")
    
    print("""
    ----------------------------------------
    Select the type of edit you want to apply:
    1. Drawing     [Enter 'd']
    2. Vintage     [Enter 'v']
    3. Cinematic   [Enter 'c']
    ----------------------------------------
    """)
    
    typeEdit = input("> Please enter your choice: ").strip().lower()
    
    while typeEdit not in ['d', 'v', 'c']:
        print("\nInvalid choice. Please select one of the following options: d, v, c.")
        typeEdit = input("> Please enter your choice: ").strip().lower()
    
    return typeEdit

editType = startEditing()
editBatch(pathIn,pathOut, editType)