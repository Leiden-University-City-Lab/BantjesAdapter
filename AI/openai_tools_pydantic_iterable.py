import datetime
import json
import os
import re
from typing import List, Optional, Iterable
import instructor
import openai
from os.path import join, dirname
from dotenv import load_dotenv

from instructor import OpenAISchema
from pydantic import Field, ValidationError

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

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


class Particularity(OpenAISchema):
    particularity: Optional[str] = Field(None, description="Extra information, mentioned after Bijzonderheden")
    source: Optional[str] = Field(None, description='The source of the info mentioned in parentheses, e.g. (6)')


class Parent(OpenAISchema):
    """Identifying information about the parent."""

    first_name: Optional[str] = Field(None, description="The first name of a person, e.g. Cornelis")
    last_name: Optional[str] = Field(None, description="The last name of a person, e.g. EKAMA")
    extra_info: Optional[str] = Field(None, description="Extra info about that specific person such as birth/death date education and job.")
    source: Optional[str] = Field(None, description='The source of the info mentioned in parentheses, e.g. (6)')


class Career(OpenAISchema):
    job: Optional[str] = Field(None, description='The type of job, e.g. Lector Wis-,Natuur- en Zeevaartkunde')
    location: Optional[str] = Field(None, description='The location of the job, e.g. Leiden')
    date: Optional[str] = Field(None, description='The date of the job')
    source: Optional[str] = Field(None, description='The source of the info mentioned in parentheses, e.g. (6)')


class Spouse(OpenAISchema):
    """Identifying information about a person."""

    first_name: str = Field(..., description="The first name of a person, e.g. Cornelis")
    second_name: Optional[str] = Field(..., description="The second name of a person witten in parentheses, e.g.jacob in Jacobus(Jacob)")
    last_name: str = Field(..., description="The last name of a person, e.g. EKAMA")
    alternative_last_name: Optional[str] = Field(..., description="The alternative last name of a person witten in parentheses, e.g. GOOL in GOLIUS (GOOL)")
    birth_date: Optional[str] = Field(None, description="The birth date of the peron, mentioned after geb. e.g. 28-03-1794")
    birth_place: Optional[str] = Field(None, description="The birth place of the peron")
    baptized_date: Optional[str] = Field(None, description="The date in which this person has been baptized, mentioned after ged. e.g. 28-03-1794")
    death_date: Optional[str] = Field(None, description="The death date of the peron mentioned after gest.")
    death_place: Optional[str] = Field(None, description="The place where this person has died")
    marriage: Optional[str] = Field(None, description="which marriage is this. ex: getr. 1")
    extra_info: Optional[str] = Field(None, description="Extra info about that specific person such as education and job.")
    source: Optional[str] = Field(None, description='The source of the info mentioned in parentheses, e.g. (6)')


class Education(OpenAISchema):
    study: Optional[str] = Field(None, description='The subject of study, e.g. Stud.Theol.')
    location: Optional[str] = Field(None, description='The location of study, e.g. Leiden')
    date: Optional[str] = Field(None, description='The date of the education')
    source: Optional[str] = Field(None, description='The source of the info mentioned in parentheses, e.g. (6)')


class PersonInfo(OpenAISchema):
    """"Correctly extracted person information"""
    first_name: str = Field(..., description="The first name of a person, e.g. Cornelis")
    last_name: str = Field(..., description="The last name of a person, e.g. EKAMA")
    birth_date: Optional[str] = Field(None, description="The birth date of a person, e.g. 28-03-1794")
    birth_place: Optional[str] = Field(None, description="The birth place of the peron")
    baptized_date: Optional[str] = Field(None, description="The date in which this person has been baptized, mentioned after ged. e.g. 28-03-1794")
    death_date: Optional[str] = Field(None, description="The death date of the peron mentioned after gest.")
    death_place: Optional[str] = Field(None, description="The place where this person has died")
    education: Optional[List[Education]] = Field(None, description='Education of the person, mentioned after Opleiding:')
    careers: Optional[List[Career]] = Field(None, description='Careers of the person, mentioned after Loopbaan:')
    particularities: Optional[List[Particularity]] = Field(None, description='extra information, mentioned after Bijzonderheden:')
    spouses: Optional[List[Spouse]] = Field(None, description='Spouses of the person, mentioned after Echtgenote:')
    parents: Optional[List[Parent]] = Field(None, description='Information about a persons mother or father, mentioned after Ouders:')
    grand_parents_father: Optional[List[Parent]] = Field(None, description="Information about a person's grand mother or grand father, mentioned after Ouders Vader:")
    grand_parents_mother: Optional[List[Parent]] = Field(None, description="Information about a person's grand mother or grand father, mentioned after Ouders Moeder:")
    in_laws: Optional[List[Parent]] = Field(None, description="Information about a person's mother in-law or  father in-law, mentioned after Ouder(s) Echtgenote(s):")
    children: Optional[List[Parent]] = Field(None, description="Information about a person's children, mentioned after Kinderen:")
    far_family: Optional[List[Parent]] = Field(None, description="Information about a person's far family, mentioned after Verdere familie:")


input_directory = '../bantjes_data/text/vol4/output'
output_directory = '../bantjes_data/text/vol4/json'
file_count = 1

person_files = sorted(os.listdir(input_directory), key=lambda x: int(re.search(r'(\d+)\.txt', x).group(1)))

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
                    response_model=Iterable[PersonInfo],
                    tool_choice="auto"
                )

                # Save person info in json
                for person in completion:
                    print(f'Processing person {file_count}')
                    save_person_info(json.dumps(person.model_dump(), indent=2), output_directory, file_count)
                    file_count += 1
            except ValidationError as e:
                print('Error occurred!')
                print(e)


# output = PersonInfo.from_response(response)

# print(type(completion))
# print(json.dumps(completion.model_dump(), indent=1))

#output = response.choices[0].message
