# This file contains the code that converts PDFs to PNG and processes the png using cv2

import cv2
import os
from pdf2image import convert_from_path

# directory containing the pdfs
input_directory_pdf = ["bantjes_data/pdf/vol1.pdf",
                   "bantjes_data/pdf/vol2.pdf",
                   "bantjes_data/pdf/vol3.pdf",
                   "bantjes_data/pdf/vol4.pdf",
                   "bantjes_data/pdf/vol5.pdf",
                   "bantjes_data/pdf/vol6.pdf",
                   "bantjes_data/pdf/vol7.pdf"]


# Function to convert PDF to PNG images
def pdf_to_png(pdf_path, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    pages = convert_from_path(pdf_path)

    for i, page in enumerate(pages):
        page.save(os.path.join(output_dir, f"page_{i+1}.png"), "PNG")

# Iterate through each PDF file
# for pdf_path in input_directory_pdf:
#     # Create output directory based on PDF file name
#     output_dir = os.path.splitext(os.path.basename(pdf_path))[0]
#     output_dir = os.path.join("bantjes_data/png_unprocessed", output_dir)
#
#     # Convert PDF to PNG images and save them in the output directory
#     pdf_to_png(pdf_path, output_dir)
#
# print("Conversion completed successfully.")


# Function to process each image
def process_image(image_path, output_directory):
    # Load the image
    image = cv2.imread(image_path)

    # Denoise image with OpenCV
    denoise = cv2.fastNlMeansDenoisingColored(image, None, 5, 5, 7, 21)

    # Convert image to grayscale
    gray = cv2.cvtColor(denoise, cv2.COLOR_BGR2GRAY)

    # Grayscale to binary with OpenCV threshold
    th, image = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    # Extract volume information from the image path
    volume = image_path.split('/')[-2]

    # Create the directory for the volume if it doesn't exist
    volume_output_directory = os.path.join(output_directory, volume)
    if not os.path.exists(volume_output_directory):
        os.makedirs(volume_output_directory)

    # Save the processed image to the output directory
    output_image_path = os.path.join(volume_output_directory, os.path.basename(image_path))
    cv2.imwrite(output_image_path, image)


# List of input directories
input_directory_unprocessed = [
    # "../bantjes_data/png_unprocessed/vol1"
    "../bantjes_data/png_unprocessed/vol2",
    # "../bantjes_data/png_unprocessed/vol3",
    # "../bantjes_data/png_unprocessed/vol4",
    # "../bantjes_data/png_unprocessed/vol5",
    # "../bantjes_data/png_unprocessed/vol6",
    # "../bantjes_data/png_unprocessed/vol7"
]

# Output directory for processed images
output_directory = "../bantjes_data/png_processed/vol2"

# Process images in each input directory
for input_dir in input_directory_unprocessed:
    # List all files in the input directory
    files = os.listdir(input_dir)
    # Process each image in the directory
    for file in files:
        # Process the image and save it to the output directory
        process_image(os.path.join(input_dir, file), output_directory)
