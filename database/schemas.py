from typing import Optional, List, Literal
from enum import IntEnum
from instructor import OpenAISchema
from pydantic import Field, ConfigDict


class Particularity(OpenAISchema):
    """Identifying extra information about a person."""

    particularity: Optional[str] = Field(None, description="Extra information, mentioned after Bijzonderheden", examples=['Salaris: f 800'])
    location: Optional[str] = Field(None, description='The location mentioned for this particularity', examples=['Leiden'])
    date: Optional[str] = Field(None, description='The date mentioned for this particularity. In this format: 1849-01-15 or just the year', examples=['1601-10-20', '1601', '1601-10'])
    source: Optional[str] = Field(None, description='The source of the info mentioned in parentheses', examples=['6'])


class Career(OpenAISchema):
    """Identifying information about the person's career."""

    job: Optional[str] = Field(None, description='The type of job', examples=['Hoogleraar Geschiedenis'])
    location: Optional[str] = Field(None, description='The location of the job', examples=['Leiden'])
    date: Optional[str] = Field(None, description='The date of the job. In this format: 1849-01-15 or just the year', examples=['1601-10-20', '1601', '1601-10'])
    source: Optional[str] = Field(None, description='The source of the info mentioned in parentheses', examples=['6'])
    # vol1
    is_side_job: Optional[int] = Field(0,
                                        description='If it is mentioned under Nevenfuncties the value should be 1')
    # vol2-7
    # type_job: type_of_job = Field(None, description='Is this the main job mentioned by Loopbaan or a side job mentioned by Nevenfuncties?')


class Education(OpenAISchema):
    subject: Optional[str] = Field(None, description='The subject of study', examples=['Stud.Theol.'])
    location: Optional[str] = Field(None, description='The location of study', examples=['Leiden'])
    date: Optional[str] = Field(None, description='The date of the education. In this format: 1849-01-15 or just the year', examples=['1601-10-20', '1601', '1601-10'])
    source: Optional[str] = Field(None, description='The source of the info mentioned in parentheses', examples=['6'])


class Family(OpenAISchema):
    """Identifying information about the person's family."""

    FirstName: str = Field(..., description="The first name of a person", examples=['Cornelis', 'Johannes'])
    LastName: str = Field(..., description="The last name of a person. If this is this is mentioned under 'Kinderen', you should take the last name of the main person(father)", examples=['EKAMA'])
    Affix: Optional[str] = Field(None, description="The affix of a person.", examples=['van der', 'van den'])
    Gender: Optional[str] = Field(None, description="The gender of the person, based on their first name. The name are old dutch names.", examples=['Man', 'Vrouw'])
    source: Optional[str] = Field(None, description='The source of the info mentioned in parentheses', examples=['6'])
    second_names: Optional[List[str]] = Field([],
                                              description="The second names of a person separated by commas", examples=["'Jacob' in Jacobus (Jacob)"])
    alternative_last_names: Optional[List[str]] = Field([],
                                                 description="The alternative last name of a person separated by commas", examples=["'HERMINIUS' in ARMINIUS (HERMINIUS)"])
    BirthCountry: Optional[str] = Field(None, description="Fill in the birth country based on the mentioned birth city. It should be in dutch", examples=['Nederland'])
    BirthCity: Optional[str] = Field(None, description="City of birth. Usually found after Geb.", examples=['Leiden'])
    BirthDate: Optional[str] = Field(None, description="Birth date, Usually found after Geb.", examples=['1601-10-20', '1601', '1601-10'])
    DeathDate: Optional[str] = Field(None, description='Death date, Usually found Gest', examples=['1601-10-20', '1601', '1601-10'])
    DeathCity: Optional[str] = Field(None, description='City of death, Usually found "Gest."', examples=['Leiden'])


class Person(OpenAISchema):
    """"Correctly extracted person information"""
    model_config = ConfigDict(from_attributes=True)

    FirstName: str = Field(..., description="The first name of a person, mentioned after the last name",
                           examples=['Cornelis', 'Johannes'])
    LastName: str = Field(..., description="The last name of a person,mentioned in all capital letters",
                          examples=['EKAMA'])
    Affix: Optional[str] = Field(None, description="The affix of a person", examples=['van der', 'van den'])
    Gender: Optional[str] = Field("Man", description="The gender of the person, based on their first name.The name are old dutch names.", examples=['Man', 'Vrouw'])
    second_names: Optional[List[str]] = Field([], description="The second names of a person separated by commas",examples=["'Jacob' in Jacobus (Jacob)"])
    alternative_last_names: Optional[List[str]] = Field([], description="The alternative last name of a person separated by commas", examples=["'HERMINIUS' in ARMINIUS (HERMINIUS)"])
    education: Optional[List[Education]] = Field([], description='Education of the person, mentioned after Opleiding')
    careers: Optional[List[Career]] = Field([], description='Careers of the person, mentioned after Carrière or Loopbaan')
    particularities: Optional[List[Particularity]] = Field([], description='Extra information about the person mentioned after Bijzonderheden')
    spouses: Optional[List[Family]] = Field([], description='Spouse(s) of the person, mentioned after Echtgenote(s)')
    parents: Optional[List[Family]] = Field([], description="Information about a person's mother or father, mentioned after Ouders, Vader or Moeder")
    grand_parents: Optional[List[Family]] = Field([], description="Information about a person's grand mother or grand father, mentioned after Grootouders, Grootvader, Grootmoeder or Vader Vader")
    # use for vol2,3,4,5,6,7
    # grand_parents_mother: Optional[List[Family]] = Field(None, description="Information about a person's grand mother or grand father, mentioned after Ouders Moeder:")
    # grand_parents_vader: Optional[List[Family]] = Field(None, description="Information about a person's grand mother or grand father, mentioned after Ouders Vader:")
    in_laws: Optional[List[Family]] = Field([], description="Information about a person's mother in-law or father in-law, mentioned after Ouder(s) Echtgenote(s)")
    children: Optional[List[Family]] = Field([], description="Information about a person's child(ren), mentioned after Kinderen")
    far_family: Optional[List[Family]] = Field([], description="Information about a person's far family, mentioned after Verdere familie")
    # vol1-5
    # type_of_person: int = 1
    # vol6
    # type_of_person: int = 4
    # vol7
    type_of_person: int = 3
    # should be changed for every volume
    # vol1
    # faculty: str = "Theologie"
    # vol2
    # faculty: str = "Medicijnen"
    # vol3
    # faculty: str = "Rechten"
    # vol4
    # faculty: str = "Wiskunde En Natuurwetenschappen"
    # vol5
    # faculty: str = "Letteren"
    # vol6 or maybe none
    # faculty: str = "Addenda"
    # vol7 or maybe none
    faculty: str = "Curatoren"
    BirthCountry: Optional[str] = Field(None, description="Fill in the birth country based on the mentioned birth city. It should be in dutch", examples=['Nederland'])
    BirthCity: Optional[str] = Field(None, description='City of birth, e.g. Leiden. Mentioned after Geb', examples=['Leiden'])
    BirthDate: Optional[str] = Field(None, description='Birth date, Mentioned after Geb', examples=['1601-10-20', '1601', '1601-10'])
    DeathDate: Optional[str] = Field(None, description='Death date, Mentioned after Gest', examples=['1601-10-20', '1601', '1601-10'])
    DeathCity: Optional[str] = Field(None, description='City of death, e.g. Leiden.Mentioned after Gest', examples=['Leiden'])
