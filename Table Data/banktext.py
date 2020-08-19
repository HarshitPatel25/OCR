# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 15:38:38 2020

@author: Harshit
"""

from PIL import Image
import pytesseract as pt
import argparse
import cv2
import ftfy
import os
import re
import io
import json

#Construct and Parse The Argument 
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--image", required = True, help = "Path to the image")

args = vars(parser.parse_args())

# Load an color image in grayscale 
img = cv2.imread(args["image"],0)

filename = "55012.png".format(os.getpid())
print(filename)
#cv2.imwrite(filename, img)

# Load the image using PIL (Python Imaging Library), Apply OCR, and then delete the temporary file
pt.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
text = pt.image_to_string(Image.open(filename))
res = text.split() 
print(res)
os.remove(filename)


text_output = open('bankopt.txt', 'w', encoding='utf-8')
text_output.write(text)

text = ftfy.fix_text(text)
text = ftfy.fix_encoding(text)
'''for god_damn in text:
    if nonsense(god_damn):
        text.remove(god_damn)
    else:
        print(text)'''
        
        
# Initializing data variable
Name = None
Address = None
Account = None
IFSC = None
AccSt= None
nameline = []
dobline = []
AccStline = []
text0 = []
text1 = []
text2 = []

lines = text.split('\n')
for lin in lines:
    s = lin.strip()
    s = lin.replace('\n','')
    s = s.rstrip()
    s = s.lstrip()
    text1.append(s)
    

text1 = list(filter(None, text1))

lineno = 0  # to start from the first line of the text file.

for wordline in text1:
    xx = wordline.split('\n')
    if ([w for w in xx if re.search('(Name @|Costumer Name|ame|name|costumer|User Name|Nam|Customer Name|bank)$', w)]):
        text1 = list(text1)
        lineno = text1.index(wordline)
        break

# text1 = list(text1)
text0 = text1[lineno+1:]
print(text0)  # Contains all the relevant extracted text in form of a list - uncomment to check

def findword(textlist, wordstring):
    lineno = -1
    for wordline in textlist:
        xx = wordline.split( )
        if ([w for w in xx if re.search(wordstring, w)]):
            lineno = textlist.index(wordline)
            textlist = textlist[lineno+1:]
            return textlist
    return textlist


try:

    # Cleaning first names, better accuracy
    Name = text0[0]
    Name = Name.rstrip()
    Name = Name.lstrip()
    Name = Name.replace("8", "B")
    Name = Name.replace("0", "D")
    Name = Name.replace("6", "G")
    Name = Name.replace("1", "I")
    Name = re.sub('[^a-zA-Z] +', ' ', Name)

    # Cleaning Father's name
    Address = text0[1]
    Address = Address.rstrip()
    Address = Address.lstrip()
    Address = Address.replace("8", "S")
    Address = Address.replace("0", "O")
    Address = Address.replace("6", "G")
    Address = Address.replace("1", "I")
    Address = Address.replace("\"", "A")
    Address = re.sub('[^a-zA-Z] +', ' ', Address)

    # Cleaning DOB
    Account = text0[2]
    Account = Account.rstrip()
    Account = Account.lstrip()
    Account = Account.replace('|', ' ')
    Account = Account.replace('\"', '/1')
    Account = Account.replace(" ", "")

    # Cleaning PAN Card details
    AccSt = findword(text1, '(From|To|riod|Period|rom|Statement|Account statement|tetement|state|Account|for)$')
    AccStline = text0[0]
    AccSt = AccStline.rstrip()
    AccSt = AccSt.lstrip()
    AccSt = AccSt.replace(" ", "")
    AccSt = AccSt.replace("\"", "")
    AccSt = AccSt.replace(";", "")
    AccSt = AccSt.replace("%", "L")

except:
    pass

# Making tuples of data
data = {}
data['Name'] = Name
data['Address'] = Address
data['Account'] = Account
data['AccSt'] = AccSt


 


# Writing data into JSON
try:
    to_unicode = unicode
except NameError:
    to_unicode = str

# Write JSON file
with io.open('data.json', 'w', encoding='utf-8') as outfile:
    str_ = json.dumps(data, indent=4, sort_keys=True, separators=(',', ': '), ensure_ascii=False)
    outfile.write(to_unicode(str_))

# Read JSON file
with open('data.json', encoding = 'utf-8') as data_file:
    data_loaded = json.load(data_file)

# print(data == data_loaded)

# Reading data back JSON(give correct path where JSON is stored)
with open('data.json', 'r', encoding= 'utf-8') as f:
    ndata = json.load(f)

print(ndata)


print('\t', "|+++++++++++++++++++++++++++++++|")
print('\t', '|', '\t', ndata['Name'])
print('\t', "|-------------------------------|")
print('\t', '|', '\t', ndata['Address'])
print('\t', "|-------------------------------|")
print('\t', '|', '\t', ndata['Account'])
print('\t', "|-------------------------------|")
print('\t', '|', '\t', ndata['AccSt'])
print('\t', "|+++++++++++++++++++++++++++++++|")
