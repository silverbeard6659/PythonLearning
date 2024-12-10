import numpy as np
import cv2 as cv
import os

print(cv.__version__)
# path = r'C:\Users\\shdwspr\\Desktop\\pythonPCИльин\\photo_2024-12-10_01-35-21.jpg'
# path = r'C:\\Users\\shdwspr\\Desktop\\pythonPCИльин\\geeks14.png'
# img = cv.imread('C:\\Users\\shdwspr\\Desktop\\pythonPCИльин\\photo_2024-12-10_01-35-21.jpg')
# assert img is not None, "file could not be read, check with os.path.exists()"  
# path = r'.Screenshot_2.png'
# src = cv.imread(path)
# window_name = 'Image'
# image = cv.cvtColor(src, cv.COLOR_BAYER_BG2GRAY)
# cv.imshow(window_name, image)
# cv.imshow('image', img)
# cv.waitKey(0)
img = cv.imread('geeks14.png')

# Check if image was loaded properly
if img is not None:
    print('Image loaded successfully!')
else:
    print('Failed to load image.')
    
# def locateImage():
    
    

# cv.imshow('geeks14.png', img)
# cv.waitKey(0)