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


def save_person_info(text, metadata, file_count):
    # Create a filename using last name and first name
    file_name = f"{file_count}.txt"
    file_path = os.path.join('../bantjes_data/text/vol2', file_name)

    # Write the metadata and text to the file
    with open(file_path, 'w') as file:
        file.write(metadata + '\n')  # Write metadata
        file.write('-' * 25 + '\n')  # Write separator
        file.write(text)  # Write OCR text


def process_images(directory):
    file_count = 1
    person_last_name = None
    person_text = ''
    person_images = []

    # List all files in the directory
    all_files = os.listdir(directory)

    # Filter only the PNG files
    png_files = [file for file in all_files if file.endswith('.png')]

    # Sort the PNG files
    sorted_files = sorted(png_files, key=lambda x: int(x.split('_')[1].split('.')[0]))

    # Iterate through each image in the sorted list
    for filename in sorted_files:
        if filename.endswith(".png"):
            image_path = os.path.join(directory, filename)
            ocr_text = perform_ocr(image_path)

            # Check if the OCR text starts with a last name
            lines = ocr_text.split('\n')
            first_line = lines[0].strip()
            second_line = lines[1].strip()
            third_line = lines[2].strip()

            if re.match(r'\b[A-Z]{2,}', first_line) or re.match(r'\b[A-Z]{2,}', second_line) or re.match(r'\b[A-Z]{2,}', third_line):
                # Save previous person's information if it exists
                if person_last_name:
                    # Concatenate image paths as metadata
                    image_metadata = '\n'.join(person_images)
                    save_person_info(person_text, image_metadata, file_count)
                    file_count += 1

                # Start accumulating information for the new person
                person_last_name = first_line
                person_text = ocr_text
                person_images = [image_path]  # Reset person_images list
            else:
                # Append image path to person_images list
                person_images.append(image_path)
                # Append the text to the current person's information
                person_text += '\n' + ocr_text

    # Save the last person's information
    if person_last_name:
        # Concatenate image paths as metadata
        image_metadata = '\n'.join(person_images)
        save_person_info(person_text, image_metadata, file_count)


# directory containing the images
image_directory = '../bantjes_data/png_processed/vol2/person'

# Process the images and save information related to each person
process_images(image_directory)
# text= perform_ocr('../bantjes_data/png_processed/vol5/first_persons/page_11.png')
# print(text)
