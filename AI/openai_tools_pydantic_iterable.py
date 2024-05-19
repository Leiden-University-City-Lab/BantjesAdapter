import os
import re
import sys
from datetime import datetime
from typing import Iterable
import instructor
from instructor.retry import InstructorRetryException
import openai
from os.path import join, dirname
from dotenv import load_dotenv

from database import schemas
from database.schemas import Person
from database.crud import get_person, update_person, update_education, get_education_count, get_particularity_count, \
    update_particularity, get_maybe_same_person, get_career_count, update_career, create_person, create_relation, \
    create_location
from pydantic import ValidationError

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Add your own OpenAI API key
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = openai.OpenAI()
client = instructor.from_openai(client, mode=instructor.Mode.TOOLS)


def format_birth_date(date_str):
    format_ddmmyyyy = "%d-%m-%Y"
    format_yyyymmdd = "%Y-%m-%d"

    if len(date_str) != 10:
        return None

    try:
        date_obj = datetime.strptime(date_str, format_ddmmyyyy)
        return date_obj.strftime(format_yyyymmdd)
    except ValueError:
        pass

    try:
        date_obj = datetime.strptime(date_str, format_yyyymmdd)
        return date_str
    except ValueError:
        return None


def extract_birth_year(birth_date: str):
    if birth_date is not None:
        # Try to extract birth year from birth_date using regex
        match = re.search(r'\b\d{4}\b', birth_date)
        if match:
            return match.group(0)
        else:
            return None


def save_person_info(text, directory, file_counter):
    file_name = f"{file_counter}.txt"

    file_path = os.path.join(directory, file_name)

    # Write the text to the file
    with open(file_path, 'a') as output_file:
        output_file.write('\n\n' + '-' * 25 + '\n')  # Write separator
        output_file.write(text)


def chat_completion(person_info):
    # Pass person_data to OpenAI
    return client.chat.completions.create(
        model="gpt-3.5-turbo",
        # model="gpt-4o",
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
                "content": f'The data of the following person or persons: {person_info}'
            }
        ],
        response_model=Iterable[Person],
        max_retries=1,
        tool_choice="auto"
    )


def enrich_relations(family: schemas.Family, person_from_db):
    if hasattr(family, "BirthCity"):
        family_birth_place = family.BirthCity
    else:
        family_birth_place = None

    family_db = create_person(family)
    create_relation(person_from_db.personPersonID, family_db.personPersonID, 3)
    create_location(family_db.personPersonID, format_birth_date(family.BirthDate), 1,
                    family_birth_place)

    if family.DeathDate:
        create_location(family_db.personPersonID, format_birth_date(family.DeathDate), 2,
                        family.DeathCity)


input_directory = '../bantjes_data/text/vol1'
file_count = 1

person_files = sorted(os.listdir(input_directory),
                      key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else float('inf'))

for index, filename in enumerate(person_files):
    if index == 0 and filename.endswith('.txt'):
        with open(os.path.join(input_directory, filename), 'r') as input_file:
            # Read the person data
            person_data = input_file.read()

            try:
                for person in chat_completion(person_data):
                    print(f'Processing person {file_count}')

                    # Verify birth_year of person
                    extracted_birth_year = extract_birth_year(person.BirthDate)

                    # Get person from database
                    get_person_from_db = get_person(person.LastName, person.FirstName, extracted_birth_year,
                                                    person.BirthCity)

                    if get_person_from_db:
                        # Access query response from database
                        person_db, location_db = get_person_from_db

                        # Update person table
                        person_db = update_person(person, person_db)

                        # Update education table
                        count = get_education_count(person_db.personPersonID)
                        if count == 0 and person.education:
                            update_education(person, person_db.personPersonID)
                        else:
                            print("Education already exists.")

                        # Update particularity table
                        count = get_particularity_count(person_db.personPersonID)
                        if count == 0 and person.particularities:
                            update_particularity(person, person_db.personPersonID)
                        else:
                            print("Particularity already exists.")

                        # Update career table
                        count = get_career_count(person_db.personPersonID)
                        if count == 0 and person.careers:
                            update_career(person, person_db.personPersonID)
                        else:
                            print("Career already exists.")

                        # Update relations
                        for spouse in person.spouses:
                            enrich_relations(spouse, person_db)

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

                    else:
                        get_maybe_same_person_from_db = get_maybe_same_person(person.LastName, person.FirstName,
                                                                              extracted_birth_year,
                                                                              person.BirthCity)
                        if get_maybe_same_person_from_db:
                            # create new person but add 'same_person' relation

                            person_db, location_db = get_maybe_same_person_from_db

                        else:
                            sys.exit()  # create person











                    # save_person_info(json.dumps(person.model_dump(), indent=2), input_directory, file_count)
                    file_count += 1

                    # get_person_info = get_person(person.FamilyName, person.FirstName)
                    # print(json.dumps(get_person_info))

            except InstructorRetryException as e:
                print(e)
                print("Retry attempts: ", e.n_attempts)
                print("Last completion: ", e.last_completion)
                pass

# output = PersonInfo.from_response(response)

# print(type(completion))
# print(json.dumps(completion.model_dump(), indent=1))

# output = response.choices[0].message
