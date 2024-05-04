import datetime
import json
import os
import re
import sys
from typing import List, Optional, Iterable
import instructor
import openai
from os.path import join, dirname
from dotenv import load_dotenv

from database.schemas import Person
from database.crud import get_person

from instructor import OpenAISchema
from pydantic import Field, ValidationError

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

sys.exit()

# Add your own OpenAI API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = openai.OpenAI()
client = instructor.from_openai(client, mode=instructor.Mode.TOOLS)


def save_person_info(text, directory, count):
    file_name = f"{count}.json"

    file_path = os.path.join(directory, file_name)

    # Write the text to the file
    with open(file_path, 'w') as output_file:
        output_file.write(text)


input_directory = '../bantjes_data/text/vol1'
output_directory = '../bantjes_data/text/vol1/json'
file_count = 1


person_files = sorted(os.listdir(input_directory), key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else float('inf'))

for filename in person_files:
    if filename.endswith('.txt'):
        with open(os.path.join(input_directory, filename), 'r') as input_file:
            # Read the person data
            person_data = input_file.read()
            # Pass person_data to OpenAI

            try:
                completion = client.chat.completions.create(
                    model="gpt-3.5-turbo-1106",
                    messages=[
                        {
                            "role": "user",
                            "content": f'''Extract person data.
                                - The data can contain multiple persons
                                - In case of multiple persons, you can identify each person by surname
                                - The surname is always with capitals followed by the middle / first name
                                
                                The data of the following person or persons: {person_data}'''
                        }
                    ],
                    response_model=Iterable[Person],
                    tool_choice="auto"
                )

                # Save person info in json
                for person in completion:
                    print(f'Processing person {file_count}')
                    save_person_info(json.dumps(person.model_dump(), indent=2), output_directory, file_count)
                    file_count += 1

                    get_person_info = get_person(person.FamilyName, person.FirstName)
                    print(json.dumps(get_person_info))


            except ValidationError as e:
                print('Error occurred!')
                print(e)

# output = PersonInfo.from_response(response)

# print(type(completion))
# print(json.dumps(completion.model_dump(), indent=1))

# output = response.choices[0].message
