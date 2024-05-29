import json
import os
from instructor.retry import InstructorRetryException

from AI import client
from database.schemas import Person
from database.crud import get_person, get_maybe_same_person, create_person
from helpers.person import save_person_info, extract_birth_year, enrich_personal_information, update_relations


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


def process_person_data(volume):
    input_directory = f'bantjes_data/text/{volume}'
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
                        enrich_personal_information(person, person_db)

                        # Update relations
                        update_relations(person, person_db)

                    else:
                        get_maybe_same_person_from_db = get_maybe_same_person(person.LastName, person.FirstName,
                                                                              person.alternative_last_names,
                                                                              person.second_names,
                                                                              extracted_birth_year,
                                                                              person.BirthCity)
                        if get_maybe_same_person_from_db:
                            maybe_same_person_db = create_person(person)
                            enrich_personal_information(person, maybe_same_person_db)

                            # Update relations
                            update_relations(person, maybe_same_person_db, True)

                        else:
                            new_person_db = create_person(person)
                            enrich_personal_information(person, new_person_db)

                            update_relations(person, new_person_db)

                    print(f'Finished processing person {file_count} with name {person.FirstName} {person.LastName}')

                    file_count += 1

                except InstructorRetryException as e:
                    print(e)
                    print("Retry attempts: ", e.n_attempts)
                    print("Last completion: ", e.last_completion)
                    file_count += 1
                    pass
