import os
import re
from datetime import datetime
from database import schemas
from database.crud import update_person, update_education, get_education_count, get_particularity_count, \
    update_particularity, get_career_count, update_career, create_person, create_relation, \
    create_location, get_relations_count


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


# def save_person_info(text, directory, file_counter, volume):
#     file_name = f"{file_counter}.{volume}.json"
#
#     file_path = os.path.join(directory, file_name)
#     print(f'Write person info to: {file_path}')
#
#     # Write the text to the file
#     with open(file_path, 'w') as output_file:
#         output_file.write(text)


def save_person_info(person_json, new_directory, file_count, volume):
    if not os.path.exists(new_directory):
        os.makedirs(new_directory)

    json_filename = f'{file_count}.{volume}.json'
    with open(os.path.join(new_directory, json_filename), 'w') as json_file:
        json_file.write(person_json)


def update_relations(person: schemas.Person, person_db, same_person: bool = False):
    relation_count = get_relations_count(person_db.personPersonID)
    if relation_count == 0:
        print('Update relations')

        if same_person:
            enrich_relations(person, person_db, 7)

        if person.spouses is not None:
            for spouse in person.spouses:
                enrich_relations(spouse, person_db, 3)

        if person.in_laws is not None:
            for in_law in person.in_laws:
                enrich_relations(in_law, person_db, 4)

        if person.grand_parents is not None:
            for grand_parent in person.grand_parents:
                enrich_relations(grand_parent, person_db, 2)

        if person.parents is not None:
            for parent in person.parents:
                enrich_relations(parent, person_db, 1)

        if person.far_family is not None:
            for far_fam in person.far_family:
                enrich_relations(far_fam, person_db, 6)

        if person.children is not None:
            for child in person.children:
                # Assign last name of person to child if not exists
                if not hasattr(child, "LastName") or child.LastName is None:
                    child.LastName = person_db.LastName

                enrich_relations(child, person_db, 5)
    else:
        print("Relations already exists.")


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


def enrich_personal_information(person, person_from_db):
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


# def join_person_names(person):
#     alternative_last_names = ' '.join(person.alternative_last_names)
#     second_names = ' '.join(person.second_names)
#     return alternative_last_names, second_names
def join_person_names(person):
    # Ensure alternative_last_names is always treated as a list
    if isinstance(person.alternative_last_names, list):
        alternative_last_names = ' '.join(person.alternative_last_names)
    else:
        alternative_last_names = str(person.alternative_last_names)  # Handle non-list case

    # Similarly, ensure second_names is treated as a list if applicable
    if isinstance(person.second_names, list):
        second_names = ' '.join(person.second_names)
    else:
        second_names = str(person.second_names)  # Handle non-list case

    return alternative_last_names, second_names
