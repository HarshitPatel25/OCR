# -*- coding: utf-8 -*-
"""
Created on Wed Aug 13 13:27:23 2020

@author: Harshit
"""

from PIL import Image
import cv2
import pytesseract as pt
import numpy as np
import re

img = Image.open("page_1.jpg")
img2 = img.crop((1132, 876, 1567, 1016))
img2.save("img2.jpg")

image = cv2.imread('img2.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Morph open to remove noise
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

# Find contours and remove small noise
cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    area = cv2.contourArea(c)
    if area < 50:
        cv2.drawContours(opening, [c], -1, 0, -1)

# Invert and apply slight Gaussian blur
result = 255 - opening
result = cv2.GaussianBlur(result, (3,3), 0)

# Perform OCR for NAME
name = pt.image_to_string(result, lang='eng', config='--psm 6')
print(name)


#################  For Pan Number  ####################

img_pan = Image.open("page_1.jpg")
img3 = img_pan.crop((189, 822, 1104, 1007))
img3.save("img3.jpg")

image = cv2.imread('img3.jpg')
result = image.copy()
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]


# Remove horizontal lines
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40,1))
remove_horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=2)
cnts = cv2.findContours(remove_horizontal, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(result, [c], -1, (255,255,255), 5)
    
    
# Remove vertical lines
vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,40))
remove_vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=2)
cnts = cv2.findContours(remove_vertical, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
for c in cnts:
    cv2.drawContours(result, [c], -1, (255,255,255), 5)



cv2.imshow('thresh', thresh)
cv2.imshow('result', result)
cv2.imwrite('result.png', result)
cv2.waitKey()

def remove(string): 
    return string.replace(" ", "") 

# Perform OCR
PAN = pt.image_to_string(result, lang='eng', config='--psm 6')
print(remove(PAN))   
