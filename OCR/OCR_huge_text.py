# this function creates a huge txt file of all the images of one book
import glob
import os
from PIL import Image
import pytesseract
import re

# Custom OCR configuration
custom_psm_config = r'--psm 4 --tessdata-dir language'

# Function to perform OCR on an image and extract text
def perform_ocr(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, config=custom_psm_config, lang='alg')
    return text.strip()

# List of directory paths
directory_paths = 'bantjes_data/png_processed/vol4/person'


# Output file path for writing OCR results
output_file_path = 'bantjes_data/text/output.txt'

# Function to process directories and perform OCR
def process_images_in_order(directory_path, output_file_path):
    # List image files and sort them based on filename
    image_files = sorted(glob.glob(os.path.join(directory_path, 'page_*.png')))
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for image_file in image_files:
            # Perform OCR on the image
            ocr_text = perform_ocr(image_file)
            # Write OCR text to the output file
            output_file.write(f'{os.path.basename(image_file)}:\n{ocr_text}\n\n')

# Call the function to process directories and perform OCR
process_images_in_order(directory_paths, output_file_path)
