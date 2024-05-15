import json
import os
import re
import sys
import time
from typing import Iterable
import instructor
import openai
from os.path import join, dirname
from dotenv import load_dotenv
from database.schemas import Person
from database.crud import get_person, update_person, update_education, get_education_count, get_particularity_count, \
    update_particularity
from pydantic import ValidationError

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Add your own OpenAI API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = openai.OpenAI()
client = instructor.from_openai(client, mode=instructor.Mode.TOOLS)


def extract_birth_year(birth_date: str):
    if birth_date is not None:
        # Try to extract birth year from birth_date using regex
        match = re.search(r'\b\d{4}\b', birth_date)
        if match:
            return match.group(0)
        else:
            return None


def save_person_info(text, directory, count):
    file_name = f"{count}.txt"

    file_path = os.path.join(directory, file_name)

    # Write the text to the file
    with open(file_path, 'a') as output_file:
        output_file.write('\n\n' + '-' * 25 + '\n')  # Write separator
        output_file.write(text)


input_directory = '../bantjes_data/text/vol1'
file_count = 1

# In case of validation errors
max_attempts = 3

person_files = sorted(os.listdir(input_directory),
                      key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else float('inf'))

for index, filename in enumerate(person_files):
    if index == 0 and filename.endswith('.txt'):
        attempt = 1
        while attempt <= max_attempts:
            try:
                with open(os.path.join(input_directory, filename), 'r') as input_file:
                    # Read the person data
                    person_data = input_file.read()

                    # Pass person_data to OpenAI
                    completion = client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        # model="gpt-4-turbo",
                        messages=[
                            {
                                "role": "system",
                                "content": f'''You're a person extracting data system.
                                    - The data can contain multiple persons
                                    - In case of multiple persons, you can identify each person by surname
                                    - The surname is always with capitals followed by the middle / first name
                                    - If you can't determine the field value, look at the examples
                                    '''
                            },
                            {
                                "role": "user",
                                "content": f'''
                                    The data of the following person or persons: {person_data}'''
                            }
                        ],
                        response_model=Iterable[Person],
                        tool_choice="auto"
                    )

                    for person in completion:
                        print(f'Processing person {file_count}')

                        # Verify birth_year of person
                        extracted_birth_year = extract_birth_year(person.location.locationStartDate)

                        # Get person from database
                        get_person_from_db = get_person(person.LastName, person.FirstName, extracted_birth_year, person.location.City)

                        # Access query response from database
                        person_db, location = get_person_from_db

                        if person_db is None:
                            sys.exit() # create person
                        else:
                            # Update person
                            updated_person = update_person(person, person_db)

                        # Update education
                        count = get_education_count(updated_person.personPersonID)
                        if count == 0 and person.education:
                            updated_education = update_education(person, updated_person.personPersonID)
                        else:
                            print("Education already exists.")

                        # Update particularity
                        count = get_particularity_count(updated_person.personPersonID)
                        if count == 0 and person.particularities:
                            updated_particularity = update_particularity(person, updated_person.personPersonID)
                        else:
                            print("Particularity already exists.")

                        # for spouse in person.spouses:
                        #     response = get_person(spouse.LastName, spouse.FirstName, '', '')

                        # if person.in_laws:
                        #     # do something
                        #
                        # if person.grand_parents:
                        #     # do something
                        #
                        # if person.children:
                        #     # do something
                        #
                        # if person.parents:
                        #     # do something
                        # if person.far_family:
                        #     # do something



                        # save_person_info(json.dumps(person.model_dump(), indent=2), input_directory, file_count)
                        file_count += 1

                        # get_person_info = get_person(person.FamilyName, person.FirstName)
                        # print(json.dumps(get_person_info))

                    break

            except ValidationError as e:
                print(f'Error occurred on attempt {attempt}:')
                print(e)
                if attempt < max_attempts:
                    print('Retrying...')
                    attempt += 1  # Increment attempt count
                    time.sleep(1)  # Add a delay between retries (if needed)
                    continue  # Continue to the next iteration of the while loop
                else:
                    print('Maximum attempts reached. Exiting...')
                    sys.exit()  # Exit the script if maximum attempts are reached


# output = PersonInfo.from_response(response)

# print(type(completion))
# print(json.dumps(completion.model_dump(), indent=1))

# output = response.choices[0].message
