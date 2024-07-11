# code to remove the infor related to the images from the beginning of the text files
import os


def process_file(filepath):
    with open(filepath, 'r') as file:
        lines = file.readlines()

    # Find the line with the dashes
    for i, line in enumerate(lines):
        if line.strip() == '-------------------------':
            # Everything after this line should be kept
            lines = lines[i+1:]
            break

    # Write the modified lines back to the file
    with open(filepath, 'w') as file:
        file.writelines(lines)

def process_directory(directory):
    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            process_file(filepath)


directory = 'sample_text_corrected'
process_directory(directory)
