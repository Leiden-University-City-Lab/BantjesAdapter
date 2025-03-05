
import json
import os
import re
import sys

from instructor.retry import InstructorRetryException

from AI import client
from database.schemas import Person
from database.crud import get_person, get_maybe_same_person, create_person
from helpers.person import save_person_info, extract_birth_year, enrich_personal_information, update_relations, \
    join_person_names

main_model_schema = Person.model_json_schema()

# print(json.dumps(main_model_schema, indent=2))
# sys.exit()

def chat_completion(person_info):

    # Pass person_data to OpenAI
    return client.chat.completions.create(
        model="gpt-3.5-turbo",  # Specify the model to use for the completion
        # model="gpt-4o",
        # model="gpt-4-turbo",
        messages=[
            {
                "role": "system",
                "content": '''You are an advanced data extraction system..
                              - You can identify each person by surname
                              - The surname is always in uppercase letters, followed by the middle and/or first name
                              - If you can't determine the field value, refer to the examples
                           '''
            },
            {
                "role": "user",
                "content": f'Please extract the data for the following person: {person_info}'
            }
        ],
        response_model=Person,  # Specify the response model to map the completion result
        max_retries=1,  # Set the maximum number of retries for the completion request
        tool_choice="auto"  # Automatically choose the tool for the completion
    )


# Define a dictionary to store enrichment information
enrichment_info = {}

def convert_json_to_sql(filename, person):

    # Extract the birth year from the person's birth date
    extracted_birth_year = extract_birth_year(person.BirthDate)

    # Join the string array by a space for alternative last names and second names
    alternative_last_names, second_names = join_person_names(person)
    person.alternative_last_names = alternative_last_names
    person.second_names = second_names

    # Get the person from the database
    get_person_from_db = get_person(person, extracted_birth_year)

    if get_person_from_db:
        print(f'Processing existing person with ID {get_person_from_db.personPersonID}')
        person_db = get_person_from_db
        enrich_personal_information(person, person_db)

        # Update relations in the database
        update_relations(person, person_db)

        # Update enrichment_info dictionary
        enrichment_info[filename] = {'person_id': person_db.personPersonID, 'new_person': False,
                                     'maybe_same_person': False}

    else:
        get_maybe_same_person_from_db = get_maybe_same_person(person, extracted_birth_year)
        if get_maybe_same_person_from_db:
            print(f'Processing existing potential person with ID {get_maybe_same_person_from_db.personPersonID}')
            maybe_same_person_db = create_person(person)
            enrich_personal_information(person, maybe_same_person_db)

            # Update relations in the database
            update_relations(person, maybe_same_person_db, True)

            # Update enrichment_info dictionary
            enrichment_info[filename] = {'person_id': maybe_same_person_db.personPersonID,
                                         'new_person': True, 'maybe_same_person': True}

        else:
            new_person_db = create_person(person)
            print(f'Processing new person with ID {new_person_db.personPersonID}')
            enrich_personal_information(person, new_person_db)

            # Update relations in the database
            update_relations(person, new_person_db)

            # Update enrichment_info dictionary
            enrichment_info[filename] = {'person_id': new_person_db.personPersonID, 'new_person': True,
                                         'maybe_same_person': False}


def process_person_data(path, volume):

    # Define input and output directories (txt -> json)
    input_directory = f'{path}{volume}'
    output_dir = 'evaluation_json/generated_json_gtp4o/try1/ocr_text/vol1'

    # Get a sorted list of person files in the input directory
    person_files = sorted(os.listdir(input_directory),
                          key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else float('inf'))

    # Iterate over each file in the person_files list
    for filename in person_files:

        print(filename)

        if filename.endswith('.txt'):

            with open(os.path.join(input_directory, filename), 'r') as input_file:

                # Read the person data from the file
                person_data = input_file.read()

                try:
                    # Extract the file count from the filename
                    file_count_match = re.search(r"(\d+)\.", filename)
                    if file_count_match:
                        file_count = file_count_match.group(1)
                    else:
                        print(f"No digits found in {filename}")
                        continue

                    # Define the path for the JSON file
                    json_file_path = os.path.join(output_dir, f'{file_count}.{volume}.json')
                    if os.path.isfile(json_file_path):
                        print("Get person from JSON file")
                        try:
                            with open(json_file_path, 'r') as json_file:
                                person_data_json = json.load(json_file)
                                person = Person(**person_data_json)
                        except ValueError as e:
                            print(e)
                    else:

                        print("Get person from OpenAI")
                        person = chat_completion(person_data)
                        save_person_info(json.dumps(person.model_dump(), indent=2), output_dir, file_count, volume)

                        # json -> sql
                        print(f'Processing person {file_count} with name {person.FirstName} {person.LastName}')
                        convert_json_to_sql(filename, person)
                        print(f'Finished processing person {file_count} with name {person.FirstName} {person.LastName}')

                except InstructorRetryException as e:
                    print(e)
                    print("Retry attempts: ", e.n_attempts)
                    print("Last completion: ", e.last_completion)
                    pass

    print(enrichment_info)

    # Save enrichment_info to a JSON file
    with open('enrichment_info_vol1n.json', 'w') as json_file:
        json.dump(enrichment_info, json_file, indent=2)

