from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import numpy as np
import os
import cv2
import random

# Input Images Dir
pathIn = os.path.join(os.getcwd(), "inputImgs")

# Edited Images Dir
pathOut = os.path.join(os.getcwd(), "editedImgs")

def editBatch(pathIn,pathOut):
    checkDirectory(pathOut)
    
    for filename in os.listdir(pathIn):
        if filename.endswith((".jpg", ".png")):
            input_path = os.path.join(pathIn, filename)
            output_path = os.path.join(pathOut, filename)
            vintageEdit(input_path, output_path)
            # drawingEdit(pathIn,pathOut)

def vintageEdit(pathIn,pathOut):
    # Open the image
    img = Image.open(pathIn).convert("RGB")
    
    # Step 1: Apply warm color grading
    r, g, b = img.split()
    r = r.point(lambda i: i * 1.2)  # Increase red tones
    g = g.point(lambda i: i * 1.1)  # Slightly increase green
    b = b.point(lambda i: i * 0.9)  # Reduce blue for a warmer feel
    img = Image.merge("RGB", (r, g, b))
    
    # Step 2: Add a slight blur
    img = img.filter(ImageFilter.GaussianBlur(0.4))
    
    # Step 3: Add film grain using NumPy
    np_img = np.array(img)
    noise = np.random.normal(0, 10, np_img.shape)  # Gaussian noise
    np_img = np.clip(np_img + noise, 0, 255).astype(np.uint8)
    img = Image.fromarray(np_img)
    
    # Step 4: Adjust brightness and contrast
    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(1.1)  # Slightly brighten
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.2)  # Increase contrast
    
    # Step 5: Add vignette using OpenCV
    rows, cols = np_img.shape[:2]
    kernel_x = cv2.getGaussianKernel(cols, cols // 3)
    kernel_y = cv2.getGaussianKernel(rows, rows // 3)
    kernel = kernel_y * kernel_x.T
    mask = 255 * kernel / np.linalg.norm(kernel)
    vignette = np.dstack((mask, mask, mask))
    np_img = cv2.addWeighted(np_img, 0.7, vignette.astype(np.uint8), 0.3, 0)
    img = Image.fromarray(np_img)
    
    # Save the edited image
    img.save(pathOut)
    print(f"Edited image saved to {pathOut}")
   

'''
///////////////
Drawing Edit //
///////////////

Purpose:
Explanation: 
Drawing Edit Purpose: This function transforms input images into hand-drawn, pencil-sketch-like pictures, using a series of image-processing steps. It creates a unique, artistic effect that highlights key features and emphasizes lines, mimicking the look of a hand-drawn sketch.

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
    for filename in os.listdir(pathIn):
        curr_file_path = os.path.join(pathIn, filename)

        try:
            with Image.open(curr_file_path) as img:
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
                img.save(os.path.join(pathOut, filename))
                print(f"Edited {filename}")
                 #-----------------------------------------#
        except:
            print(f"Error processing {filename}")

'''
This function takes two parameters: pathIn and pathOut.
- pathIn is the path to the directory containing the images to be edited.
- pathOut is the path to the directory where the edited images will be saved.
'''
def checkDirectory(pathOut):
    if not os.path.exists(pathOut):
        os.makedirs(pathOut)

# vintageEdit(pathIn,pathOut)
editBatch(pathIn,pathOut)