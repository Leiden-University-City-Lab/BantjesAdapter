from typing import Optional, List, Literal
from enum import Enum, IntEnum
from instructor import OpenAISchema
from pydantic import Field, ConfigDict

# relation = Literal['Vader', 'Moeder', 'Grootvader', 'Grootmoeder', 'Vrouw', 'Man', 'Schoonvader', 'Schoonmoeder', 'Kind', 'Verre familie']
type_of_job = Literal['Carriere', 'Nevenfuncties']


class OrderRelation(IntEnum):
    Vader = 1,
    Moeder = 2,
    Grootvader = 3,
    Grootmoeder = 4,
    Vrouw = 5,
    Man = 6,
    Schoonvader = 7,
    Schoonmoeder = 8,
    Kind = 9,
    VerreFamilie = 10


class Particularity(OpenAISchema):
    """Identifying extra information about a person."""

    particularity: Optional[str] = Field(None, description="Extra information, mentioned after Bijzonderheden")
    location: Optional[str] = Field(None, description='The location mentioned for this particularity, e.g. Leiden')
    date: Optional[str] = Field(None, description='The date mentioned for this particularity')
    source: Optional[str] = Field(None, description='The source of the info mentioned in parentheses, e.g. (6)')


class Career(OpenAISchema):
    """Identifying information about the person's career."""

    job: Optional[str] = Field(None, description='The type of job, e.g. Lector Wis-,Natuur- en Zeevaartkunde')
    location: Optional[str] = Field(None, description='The location of the job, e.g. Leiden')
    date: Optional[str] = Field(None, description='The date of the job')
    source: Optional[str] = Field(None, description='The source of the info mentioned in parentheses, e.g. (6)')
    # vol1
    type_job: type_of_job = Field(None, description='Is this the main job mentioned by Carrière or a side job mentioned by Nevenfuncties?')
    # vol2-7
    # type_job: type_of_job = Field(None, description='Is this the main job mentioned by Loopbaan or a side job mentioned by Nevenfuncties?')

class Family(OpenAISchema):
    """Identifying information about the person's family."""

    first_name: str = Field(..., description="The first name of a person, e.g. Cornelis")
    last_name: str = Field(..., description="The last name of a person, e.g. EKAMA. If this is this is mentioned under 'Kinderen', you should take the last name of the main person(father)")
    birth_date: Optional[str] = Field(None,
                                      description="The birth date of the peron, mentioned after geb. e.g. 28-03-1794")
    birth_place: Optional[str] = Field(None, description="The birth place of the peron")
    baptized_date: Optional[str] = Field(None,
                                         description="The date in which this person has been baptized, mentioned after ged. e.g. 28-03-1794")
    death_date: Optional[str] = Field(None, description="The death date of the peron mentioned after gest.")
    death_place: Optional[str] = Field(None, description="The place where this person has died")
    extra_info: Optional[str] = Field(None,
                                      description="Extra info about that specific person such as education and job.")
    relation_type: OrderRelation = Field(..., description="The type of relation from the main person to this person. So if this person in mentioned below Kinderen, "
                                                     "the relation_type from the main person to this peron will be 'Vader' if the main person is a man and 'Moeder' if a woman.")
    source: Optional[str] = Field(None, description='The source of the info mentioned in parentheses, e.g. (6)')


class Education(OpenAISchema):
    subject: Optional[str] = Field(None, description='The subject of study, e.g. Stud.Theol.')
    location: Optional[str] = Field(None, description='The location of study, e.g. Leiden', alias='City')
    date: Optional[str] = Field(None, description='The date of the education')
    source: Optional[str] = Field(None, description='The source of the info mentioned in parentheses, e.g. (6)')


class Person(OpenAISchema):
    """"Correctly extracted person information"""
    model_config = ConfigDict(from_attributes=True)

    first_name: str = Field(..., description="The first name of a person, e.g. Cornelis")
    last_name: str = Field(..., description="The last name of a person, e.g. EKAMA")
    affix: Optional[str] = Field(..., description="The affix of a person, e.g. van de, van den, van der")
    gender: Optional[str] = Field(..., description="The gender of the person, based on their names e.g. Man / Vrouw")
    second_names: Optional[str] = Field(None, description="The second names of a person separated by comma's, e.g. Jacob in Jacobus (Jacob)")
    alternative_last_names: Optional[str] = Field(None, description="The alternative last name of a person separated by comma's, e.g. HERMINIUS in ARMINIUS (HERMINIUS)")
    birth_date: Optional[str] = Field(None, description="The birth date of a person, e.g. 28-03-1794")
    birth_country: Optional[str] = Field(None, description="The birth country of the person")
    birth_city: Optional[str] = Field(None, description="The birth city of the person")
    baptized_date: Optional[str] = Field(None, description="The date in which this person has been baptized, mentioned after ged. e.g. 28-03-1794")
    death_date: Optional[str] = Field(None, description="The death date of the peron mentioned after gest.")
    death_city: Optional[str] = Field(None, description="The city where this person has died")
    death_country: Optional[str] = Field(None, description="The death country of the person")
    education: Optional[List[Education]] = Field(None, description='Education of the person, mentioned after Opleiding:')
    careers: Optional[List[Career]] = Field(None, description='Careers of the person, mentioned after Carrière: or Loopbaan:')
    side_jobs: Optional[List[Career]] = Field(None, description='Careers of the person, mentioned after Nevenfuncties:')
    particularities: Optional[List[Particularity]] = Field(None, description='extra information, mentioned after Bijzonderheden:')
    spouses: Optional[List[Family]] = Field(None, description='Spouses of the person, mentioned after Echtgenote:')
    parents: Optional[List[Family]] = Field(None, description='Information about a persons mother or father, mentioned after Ouders:')
    grand_parents: Optional[List[Family]] = Field(None, description="Information about a person's grand mother or grand father, mentioned after Grootouders:")
    # use for vol2,3,4,5,6,7
    # grand_parents_mother: Optional[List[Family]] = Field(None, description="Information about a person's grand mother or grand father, mentioned after Ouders Moeder:")
    # grand_parents_vader: Optional[List[Family]] = Field(None, description="Information about a person's grand mother or grand father, mentioned after Ouders Vader:")
    in_laws: Optional[List[Family]] = Field(None, description="Information about a person's mother in-law or  father in-law, mentioned after Ouder(s) Echtgenote(s):")
    children: Optional[List[Family]] = Field(None, description="Information about a person's children, mentioned after Kinderen:")
    far_family: Optional[List[Family]] = Field(None, description="Information about a person's far family, mentioned after Verdere familie:")
    # vol1-5
    type_of_person: int = 1
    # vol6
    # type_of_person: int = 4
    # vol7
    # type_of_person: int = 3
    # should be changed for every volume
    # vol1
    faculty: str = "Theologie"
    # vol2
    # faculty: str = "Medisch"
    # vol3
    # faculty: str = "Rechten"
    # vol4
    # faculty: str = "Wiskunde en Natuurkunde"
    # vol5
    # faculty: str = "Letteren"
    # vol6 or maybe none
    # faculty: str = "Addenda"
    # vol7 or maybe none
    # faculty: str = "Curatoren"
