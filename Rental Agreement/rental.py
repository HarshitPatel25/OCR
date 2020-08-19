# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 13:52:19 2020

@author: Harshit
"""

# import the necessary packages
from PIL import Image
import pytesseract as pt
import argparse
import cv2
import os
import re
import io
import json
import ftfy
import pyap

# from nostril import nonsense


###################################################################################
#################### Section 1: Initiate the command line interface ###############
##################################################################################

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
                help="type of preprocessing to be done, choose from blur, linear, cubic or bilateral")
args = vars(ap.parse_args())




###############################################################################
########## Section 2: Load the image -- Preprocess it -- Write it to disk #######
#################################################################################

# load the example image and convert it to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# check to see if we should apply thresholding to preprocess the
# image
if args["preprocess"] == "thresh":
    gray = cv2.threshold(gray, 0, 255,
                         cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

elif args["preprocess"] == "adaptive":
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2)
'''
What we would like to do is to add some additional preprocessing steps as in most cases, you may need to scale your 
image to a larger size to recognize small characters. 
In this case, INTER_CUBIC generally performs better than other alternatives, though it’s also slower than others.

If you’d like to trade off some of your image quality for faster performance, 
you may want to try INTER_LINEAR for enlarging images.
'''
if args["preprocess"] == "linear":
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

elif args["preprocess"] == "cubic":
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

# make a check to see if blurring should be done to remove noise, first is default median blurring




if args["preprocess"] == "blur":
    gray = cv2.medianBlur(gray, 3)

elif args["preprocess"] == "bilateral":
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

elif args["preprocess"] == "gauss":
    gray = cv2.GaussianBlur(gray, (5,5), 0)

# write the grayscale image to disk as a temporary file so we can
# apply OCR to it
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

'''
A blurring method may be applied. We apply a median blur when the --preprocess flag is set to blur. 
Applying a median blur can help reduce salt and pepper noise, again making it easier for Tesseract 
to correctly OCR the image.

After pre-processing the image, we use  os.getpid to derive a temporary image filename based on the process ID 
of our Python script.

The final step before using pytesseract for OCR is to write the pre-processed image, gray, 
to disk saving it with the filename  from above
'''

##############################################################################################################
######################################## Section 3: Running PyTesseract ######################################
##############################################################################################################


# load the image as a PIL/Pillow image, apply OCR, and then delete
# the temporary file
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
text = pt.image_to_string(Image.open(filename), lang = 'hin')
# add +hin after eng within the same argument to extract hindi specific text - change encoding to utf-8 while writing
os.remove(filename)
# print(text)

# show the output images
# cv2.imshow("Image", image)
# cv2.imshow("Output", gray)
# cv2.waitKey(0)

# writing extracted data into a text file
text_output = open('outputbase.txt', 'w', encoding='utf-8')
text_output.write(text)
text_output.close()

file = open('outputbase.txt', 'r', encoding='utf-8')
text = file.read()
# print(text)


# Cleaning all the gibberish text
text = ftfy.fix_text(text)
text = ftfy.fix_encoding(text)
   
print(text)

# Address format for the text obtained!!
regexp = "[0-9]{1,3} .+, .+, [A-Z]{2} [0-9]{6}"

# [0-9]{1,3}: 1 to 3 digits, the address number

## (space): a space between the number and the street name

## .+: street name, any character for any number of occurrences

## ,: a comma and a space before the city

## .+: city, any character for any number of occurrences

## ,: a comma and a space before the state

## [A-Z]{2}: exactly 2 uppercase chars from A to Z

## [0-9]{5}: 5 digits

## re.findall(expr, string) will return an array with all the occurrences found.

addresses = re.findall(regexp, text)
for address in addresses:
        # shows found address
        print(address)
