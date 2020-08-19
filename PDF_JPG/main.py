from pdf2jpg import pdf2jpg
inputpath = r"C:\New folder\New Vision Soft\OCR\PDF_JPG\PNB_BS.pdf"
outputpath = r"C:\New folder\New Vision Soft\OCR\PDF_JPG"

# To convert single page
result = pdf2jpg.convert_pdf2jpg(inputpath, outputpath, dpi=300, pages="1")
print(result)

# To convert multiple pages
result = pdf2jpg.convert_pdf2jpg(inputpath, outputpath, dpi=300, pages="1,0,3")
print(result)

# to convert all pages
result = pdf2jpg.convert_pdf2jpg(inputpath, outputpath, dpi=300, pages="ALL")
print(result)


from pdf2image import convert_from_path
pages = convert_from_path('PNB_BS.pdf', 500)


from pdf2image import convert_from_path
import glob

pdf_dir = glob.glob(r'C:\New folder\New Vision Soft\OCR\PDF_JPG\PNB_BS.pdf')  #your pdf folder path
img_dir = r'C:\New folder\New Vision Soft\OCR\PDF_JPG'

for pdf_ in pdf_dir:
    pages = convert_from_path(pdf_, 500)
    for page in pages:
        page.save(img_dir+pdf_.split("\\")[-1][:-3]+"jpg", 'JPEG')