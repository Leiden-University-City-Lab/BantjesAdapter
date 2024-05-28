import json
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
from pydantic_core._pydantic_core import from_json

from database import schemas
from database.schemas import Person
from database.crud import get_person, update_person, update_education, get_education_count, get_particularity_count, \
    update_particularity, get_maybe_same_person, get_career_count, update_career, create_person, create_relation, \
    create_location, get_relations_count
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

    if date_str is None or len(date_str) != 10:
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
    file_name = f"{file_counter}.json"

    file_path = os.path.join(directory, file_name)

    # Write the text to the file
    with open(file_path, 'w') as output_file:
        # output_file.write('\n\n' + '-' * 25 + '\n')  # Write separator
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
        response_model=Person,
        max_retries=1,
        tool_choice="auto"
    )


def enrich_relations(family: schemas.Family, person_from_db, type_of_relation: int):
    if hasattr(family, "BirthCity"):
        family_birth_place = family.BirthCity
    else:
        family_birth_place = None

    family_db = create_person(family)

    # type_of_relation
    # '1', 'Ouder'
    # '2', 'Grootouder'
    # '3', 'Echtgenoot'
    # '4', 'Schoonouder'
    # '5', 'Kind'
    # '6', 'Verre familie'
    # '7', 'Zelfde persoon?'

    create_relation(person_from_db.personPersonID, family_db.personPersonID, type_of_relation)

    # type_of_location
    # '1', 'Geboorteplaats'
    # '2', 'Sterfplaats'

    create_location(family_db.personPersonID, format_birth_date(family.BirthDate), 1,
                    family_birth_place)

    if family.DeathDate:
        create_location(family_db.personPersonID, format_birth_date(family.DeathDate), 2,
                        family.DeathCity)


def enrich_personal_information(person_from_db):
    # Access query response from database
    person_from_db = get_person_from_db

    # Update person table
    person_from_db = update_person(person, person_from_db)

    # Update education table
    count = get_education_count(person_from_db.personPersonID)
    if count == 0 and person.education:
        update_education(person, person_from_db.personPersonID)
    else:
        print("Education already exists.")

    # Update particularity table
    count = get_particularity_count(person_from_db.personPersonID)
    if count == 0 and person.particularities:
        update_particularity(person, person_from_db.personPersonID)
    else:
        print("Particularity already exists.")

    # Update career table
    count = get_career_count(person_from_db.personPersonID)
    if count == 0 and person.careers:
        update_career(person, person_from_db.personPersonID)
    else:
        print("Career already exists.")


input_directory = '../bantjes_data/text/vol1'
file_count = 1

person_files = sorted(os.listdir(input_directory),
                      key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else float('inf'))

for filename in person_files:
    if filename.endswith('.txt'):
        with open(os.path.join(input_directory, filename), 'r') as input_file:
            # Read the person data
            person_data = input_file.read()

            try:
                if f'{file_count}.json' in person_files:
                    print("Get person from JSON file")
                    try:
                        with open(os.path.join(input_directory, f'{file_count}.json'), 'r') as json_file:
                            person_data_json = json.load(json_file)
                            person = Person(**person_data_json)
                    except ValueError as e:
                        print(e)
                else:
                    print("Get person from OpenAI")
                    person = chat_completion(person_data)
                    save_person_info(json.dumps(person.model_dump(), indent=2), input_directory, file_count)

                print(f'Processing person {file_count} with name {person.FirstName} {person.LastName}')

                # Verify birth_year of person
                extracted_birth_year = extract_birth_year(person.BirthDate)

                # Get person from database
                get_person_from_db = get_person(person.LastName, person.FirstName, extracted_birth_year,
                                                person.BirthCity)

                if get_person_from_db:
                    person_db = get_person_from_db
                    enrich_personal_information(person_db)

                    # Update relations
                    relation_count = get_relations_count(person_db.personPersonID)
                    if relation_count == 0:
                        for spouse in person.spouses:
                            enrich_relations(spouse, person_db, 3)

                        for in_law in person.in_laws:
                            enrich_relations(in_law, person_db, 4)

                        for grand_parent in person.grand_parents:
                            enrich_relations(grand_parent, person_db, 2)

                        for parent in person.parents:
                            enrich_relations(parent, person_db, 1)

                        for far_fam in person.far_family:
                            enrich_relations(far_fam, person_db, 6)

                        for child in person.children:
                            # Assign last name of person to child if not exists
                            if not hasattr(child, "LastName") or child.LastName is None:
                                child.LastName = person_db.LastName

                            enrich_relations(child, person_db, 5)
                    else:
                        print("Relations already exists.")

                else:
                    get_maybe_same_person_from_db = get_maybe_same_person(person.LastName, person.FirstName,
                                                                          extracted_birth_year,
                                                                          person.BirthCity)
                    if get_maybe_same_person_from_db:
                        # create new person but add 'same_person' relation

                        person_db, location_db = get_maybe_same_person_from_db

                    else:
                        sys.exit()  # create person

                print(f'Finished processing person {file_count} with name {person.FirstName} {person.LastName}')

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
