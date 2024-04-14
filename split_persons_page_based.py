# This file contains the code which takes the processed images of persons info and OCRs them and then saves the info of
# person in a new .txt file.
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


# Function to save text related to a person to a text file
def save_person_info(person_name, person_text, file_count):
    file_name = f"{person_name}_{file_count}.txt"
    with open(os.path.join('bantjes_data/text/vol2/persons_split', file_name), 'w') as file:
        file.write(person_text)


def process_images(directory):
    file_count = 1
    person_name = None
    person_text = ''

    # Get a list of image filenames sorted in ascending order
    image_files = sorted(os.listdir(directory), key=lambda x: int(re.search(r'-(\d+)\.png', x).group(1)))

    # Iterate through each image in the sorted list
    for filename in image_files:
        if filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            ocr_text = perform_ocr(image_path)

            # Check if the OCR text starts with a name or a number
            lines = ocr_text.split('\n')
            first_line = lines[0].strip()

            # If the OCR text starts with a name, it's a new person
            if re.match(r'^[A-Za-z]', first_line):
                if person_name:
                    save_person_info(person_name, person_text, file_count)
                    file_count += 1
                person_name = first_line
                person_text = ocr_text
            # If the OCR text starts with a number, it's info about the same person
            elif re.match(r'^\d', first_line) and person_name:
                person_text += '\n' + ocr_text

    # Save the last person's information
    if person_name:
        save_person_info(person_name, person_text, file_count)


# Specify the directory containing the images
# image_directory = 'bantjes_data/png_processed/vol1/person'
image_directory = 'bantjes_data/png_processed/vol2/person'
# image_directory = 'bantjes_data/png_processed/vol3/person'
# image_directory = 'bantjes_data/png_processed/vol4/person'
# image_directory = 'bantjes_data/png_processed/vol5/person'
# image_directory = 'bantjes_data/png_processed/vol6/person'
# image_directory = 'bantjes_data/png_processed/vol7/person'

# Process the images and save information related to each person
process_images(image_directory)

