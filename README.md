# BantjesAdapter

The Bantjes and Poelgeest dataset is a compilation of old historical sources about professors and lectures created in 1983 written on a typing machine. 
Challenge is to capture the data of this compilation to enrich the data already loaded into the central database.

## Prerequisites

To run the program locally, the following requirements needs to be satisfied:

- **Python version:** Python 3.11
- **Dependencies:** Install the required packages listed in the `requirements.txt` file

## Installation

```bash
# Upgrade pip to the latest version
python -m pip install -U pip

# Install the required packages
pip install -r requirements.txt
```

## Run the program

Execute the program by running the `main.py` file. The main function within this file requires two arguments:

**Path:** The file path to the directory which contains different subdirectories( vol1 to vol7).\
**Volume:** The directory of the volume to be processed. This directory contains .txt files of different persons.
## Preprocessing
To preprocess the images, [`img_prep_ocr.py`](OCR/img_prep_ocr.py) is used.

## OCR

### Training Tesseract
For this project we have trained the tesseract program using a training set of image-text pairs of all the volumes. 
As our base language dataset we took the [Dutch base data](https://github.com/tesseract-ocr/langdata/tree/main/nld).
The steps that need to be followed to train Tesseract can be found [here](https://github.com/tesseract-ocr/tesstrain).


Text of the images are extracted and divided per person with the [`split_persons_img.py`](OCR/split_persons_img.py).



## OpenAI

The extracted person text is passed to the OpenAI service. 
To bring more structure to the text a Python library called instructor is used.
The instructor is built on top of Pydantic which is also used in this program.

The data is modelled as Python objects using Pydantic OpenAISchema.

When OpenAI outputs response data which doesnt match the JSON schema, the program will throw validation errors.

## Database

If the validation is passed the [`openai_tools_pydantic.py`](AI/openai_tools_pydantic.py) script will call the crud.py 
where a call to the database is initiated.
The [`__init__.py`](database/__init__.py) contains the database url and credentials. Change if required. 

## Helpers

For processing person text, such as formatting the birth date, some helper functions are created and can be located in 
the [helpers](helpers) folder. 