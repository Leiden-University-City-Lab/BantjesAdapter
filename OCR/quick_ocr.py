# simple code to perform ocr on a single page
import os
import re
from PIL import Image
import pytesseract

# Define OCR configuration
custom_psm_config = r'--psm 4 --tessdata-dir language'


# Function to perform OCR on an image and extract text
def perform_ocr(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, config=custom_psm_config, lang='alg')
    return text.strip()
ocr_text = perform_ocr('bantjes_data/png_processed/vol4/person/page_21.png')
print(ocr_text)
