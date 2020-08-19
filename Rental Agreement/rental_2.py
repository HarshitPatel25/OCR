import cv2
import pytesseract as pt
import numpy as np
import re


pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Load image, grayscale, Otsu's threshold
image = cv2.imread('stamp.jpg')
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

# Perform OCR
data = pt.image_to_string(result, lang='eng', config='--psm 6')
print(data)

p = re.compile(r'(?:Rs\.?|INR|R)\s*(\d+(?:[.,]\d+)*)|(\d+(?:[.,]\d+)*)\s*(?:Rs\.?|INR|R)')
   # ( Sample data)s = "Rs. 2000 , Rs.3000 , Rs 40,000.00 ,50,000 INR 600.25 INR"
   
   
s =  [x if x else y for x,y in p.findall(data)]

if(s[0]=='1000'):
    print(True)
else:
    print(False)
       



cv2.imshow('thresh', thresh)
cv2.imshow('opening', opening)
cv2.imshow('result', result)
cv2.waitKey()  