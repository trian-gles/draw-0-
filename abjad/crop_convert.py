from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
from PIL import Image

path = r"C:\Users\bkier\OneDrive\Desktop\poppler-21.03.0\Library\bin"

pdf_images = convert_from_path(r"C:\Users\bkier\projects\draw(0)\abjad\output_dir\base_stave.pdf", poppler_path = path)

for pdf_image in pdf_images:
    pdf_image.save(r"output_dir\staff.jpg", "JPEG")

jpeg_im = Image.open(r"C:\Users\bkier\projects\draw(0)\abjad\output_dir\staff.jpg")

width, height = jpeg_im.size

print(width, height)
im_crop = jpeg_im.crop((120, 0, 700, height))
im_crop.save(r'../resources/bkg_staff.jpg', quality=95)
