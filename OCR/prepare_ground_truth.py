import os
from PIL import Image
import pytesseract

def ocr_images(input_dir, output_dir, custom_psm_config):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Iterate over all files in input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".png"):
            # Read image using Pillow
            img_path = os.path.join(input_dir, filename)
            img = Image.open(img_path)

            # Perform OCR using pytesseract with custom PSM config
            text = pytesseract.image_to_string(img, config=custom_psm_config)

            # Write OCR text to a text file
            output_filename = os.path.splitext(filename)[0] + ".gt.txt"
            output_path = os.path.join(output_dir, output_filename)
            with open(output_path, "w") as text_file:
                text_file.write(text)

            print(f"OCR completed for {filename}. Text saved to {output_filename}")


input_directory = "/Users/zahraabedi/Desktop/screenshot_3"
output_directory = "/Users/zahraabedi/Desktop/txt_3"
custom_psm_config = r'--psm 4'
ocr_images(input_directory, output_directory, custom_psm_config)
