# This file contains the code which takes the processed images of persons info and OCRs them and then saves
# the info of person in a new .txt file. Here we use regular expressions to decide whether a page has info of a new
# person of is still about the previous person
import os
import re
from PIL import Image
import pytesseract

# Define OCR configuration
custom_psm_config = r'--psm 4 --tessdata-dir ../language'


# Function to perform OCR on an image and extract text
def perform_ocr(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, config=custom_psm_config, lang='alg')
    return text.strip()


def save_person_info(text, file_count):
    # Create a filename using last name and first name
    file_name = f"{file_count}.txt"

    file_path = os.path.join('../bantjes_data/text/vol5/output_new', file_name)

    # Write the text to the file
    with open(file_path, 'w') as file:
        file.write(text)


def process_images(directory):
    file_count = 1
    person_last_name = None
    person_text = ''

    # Get a list of image filenames sorted in ascending order
    image_files = sorted(os.listdir(directory), key=lambda x: int(re.search(r'_(\d+)\.png', x).group(1)))

    # Iterate through each image in the sorted list
    for filename in image_files:
        if filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            ocr_text = perform_ocr(image_path)

            # Check if the OCR text starts with a last name
            lines = ocr_text.split('\n')
            first_line = lines[0].strip()
            second_line = lines[1].strip()
            third_line = lines[2].strip()

            if re.match(r'^[A-Z\s\(\)]+,', first_line) or re.match(r'^[A-Z\s\(\)]+,', second_line) or re.match(r'^[A-Z\s\(\)]+,', third_line):
                # Save previous person's information if it exists
                if person_last_name:
                    save_person_info(person_text, file_count)
                    file_count += 1

                # Start accumulating information for the new person
                person_last_name = first_line
                person_text = ocr_text
            else:
                # Append the text to the current person's information
                person_text += '\n' + ocr_text

    # Save the last person's information
    if person_last_name:
        save_person_info(person_text, file_count)

# directory containing the images
# image_directory = '../bantjes_data/png_processed/vol1/person'
# image_directory = '../bantjes_data/png_processed/vol2/person'
# image_directory = '../bantjes_data/png_processed/vol3/person'
# image_directory = '../bantjes_data/png_processed/vol4/person'
image_directory = '../bantjes_data/png_processed/vol5/person'
# image_directory = '../bantjes_data/png_processed/vol6/person'
# image_directory = '../bantjes_data/png_processed/vol7/person'

# Process the images and save information related to each person
process_images(image_directory)

