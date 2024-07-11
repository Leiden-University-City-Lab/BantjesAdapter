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

# Define a dictionary to store enrichment information
enrichment_info = {}


def process_person_data(path, volume):
    input_directory = f'{path}{volume}'

    person_files = sorted(os.listdir(input_directory),
                          key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else float('inf'))

    for filename in person_files:
        if filename.endswith('.txt'):
            with open(os.path.join(input_directory, filename), 'r') as input_file:
                # Read the person data
                person_data = input_file.read()

                try:
                    file_count_match = re.search(r"(\d+)\.", filename)
                    if file_count_match:
                        file_count = file_count_match.group(1)
                    else:
                        print(f"No digits found in {filename}")
                        continue

                    if f'{file_count}.{volume}.json' in person_files:
                        print("Get person from JSON file")
                        try:
                            with open(os.path.join(input_directory, f'{file_count}.{volume}.json'), 'r') as json_file:
                                person_data_json = json.load(json_file)
                                person = Person(**person_data_json)
                        except ValueError as e:
                            print(e)
                    else:
                        print("Get person from OpenAI")
                        person = chat_completion(person_data)
                        save_person_info(json.dumps(person.model_dump(), indent=2), input_directory, file_count, volume)

                        # continue

                    print(f'Processing person {file_count} with name {person.FirstName} {person.LastName}')

                    # continue

                    # Verify birth_year of person
                    extracted_birth_year = extract_birth_year(person.BirthDate)

                    # Join the string array by a space
                    alternative_last_names, second_names = join_person_names(person)
                    person.alternative_last_names = alternative_last_names
                    person.second_names = second_names

                    # Get person from database
                    get_person_from_db = get_person(person, extracted_birth_year)

                    if get_person_from_db:
                        print(f'Processing existing person with ID {get_person_from_db.personPersonID}')
                        person_db = get_person_from_db
                        enrich_personal_information(person, person_db)

                        # Update relations
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

                            # Update relations
                            update_relations(person, maybe_same_person_db, True)

                            # Update enrichment_info dictionary
                            enrichment_info[filename] = {'person_id': maybe_same_person_db.personPersonID,
                                                         'new_person': True, 'maybe_same_person': True}

                        else:
                            new_person_db = create_person(person)
                            print(f'Processing new person with ID {new_person_db.personPersonID}')
                            enrich_personal_information(person, new_person_db)

                            update_relations(person, new_person_db)

                            # Update enrichment_info dictionary
                            enrichment_info[filename] = {'person_id': new_person_db.personPersonID, 'new_person': True,
                                                         'maybe_same_person': False}

                    print(f'Finished processing person {file_count} with name {person.FirstName} {person.LastName}')

                except InstructorRetryException as e:
                    print(e)
                    print("Retry attempts: ", e.n_attempts)
                    print("Last completion: ", e.last_completion)
                    pass
    # print(enrichment_info)
    # Save enrichment_info to a JSON file
    # with open('enrichment_info_vol7b.json', 'w') as json_file:
    #     json.dump(enrichment_info, json_file, indent=2)
