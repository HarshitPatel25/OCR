
import os
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
# From PDFInterpreter import both PDFResourceManager and PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
# Import this to raise exception whenever text extraction from PDF is not allowed
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.converter import PDFPageAggregator


import re
import pandas as pd


base_path = "C:/New folder/New Vision Soft/OCR/ITR"

my_file = os.path.join(base_path + "/" + "ITR1-Filled.pdf")
log_file = os.path.join(base_path + "/" + "pdf_log.txt")

password = ""
extracted_text = ""

# Open and read the pdf file in Binary   mode
fp = open(my_file, "rb")

# Create parser object to parse the pdf content
parser = PDFParser(fp)

# Store the parsed content in PDFDocument object
document = PDFDocument(parser, password)

# Check if document is extractable
if not document.is_extractable:
	raise PDFTextExtractionNotAllowed
	
# Create PDFResourceManager object that stores shared resources such as fonts or images
rsrcmgr = PDFResourceManager()

# set parameters for analysis
laparams = LAParams()

device = PDFPageAggregator(rsrcmgr, laparams=laparams)

# Create interpreter object to process page content from PDFDocument
# Interpreter needs to be connected to resource manager for shared resources and device 
interpreter = PDFPageInterpreter(rsrcmgr, device)

# Process the page 
for page in PDFPage.create_pages(document):
	# As the interpreter processes the page stored in PDFDocument object
	interpreter.process_page(page)
	# The device renders the layout from interpreter
	layout = device.get_result()
	#LTTextBox and LTTextLine only to use
	for lt_obj in layout:
		if isinstance(lt_obj, LTTextBox) or isinstance(lt_obj, LTTextLine):
			extracted_text += lt_obj.get_text()
			
#close the pdf file
fp.close()
			
with open(log_file, "wb") as my_log:
	my_log.write(extracted_text.encode("utf-8"))
print("Done Extrcating!!")



# Open the file that you want to search 
f = open("pdf_log.txt", "r")


# Will contain the entire content of the file as a string
content = f.read()

# remove additional space from string  
res = re.sub(' +', ' ', content)


# The regex pattern that we created
var yearReg = '(201[4-9]|202[0-9])';            # Allows a number between 2014 and 2029



# Will return all the strings that are matched
dates = re.findall(pattern, content)



for date in dates:
        print(date)
        
f.close()


################################################################################################
pdfFileObj = open('ITR-1.pdf', 'rb')  
 
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)  
    
# printing number of pages in pdf file  
print(pdfReader.numPages)  
    
# creating a page object  
pageObj = pdfReader.getPage(0)  
    
# extracting text from page  
print(pageObj.extractText())  
    
# closing the pdf file object  
pdfFileObj.close() 