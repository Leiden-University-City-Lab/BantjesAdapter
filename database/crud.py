from sqlalchemy import and_, or_, func, update
from database import Session
from .models import Person, Location, TypeOfPerson, Relation, TypeOfRelation, Education, Particularity, \
    Career, TypeOfLocation
from . import schemas

session = Session()


def get_maybe_same_person(family_name: str, first_name: str, birth_year: str, birth_place: str):
    # add table names we want to get back in the response
    return session.query(Person, Location).join(Location, and_(Location.locationPersonID == Person.personPersonID,
                                                               Person.TypeOfPerson == 1)
                                                ).outerjoin(
        TypeOfPerson,
        Person.TypeOfPerson == TypeOfPerson.PersonID
    ).filter(
        and_(Location.TypeOfLocation == 1,
             and_(
                 Person.LastName.like(f'%{family_name}%'),
                 Person.FirstName.like(f'%{first_name}%'),
                 func.extract('YEAR', Location.locationStartDate) != f'{birth_year}',
                 Location.City != f'{birth_place}'
             )
             )).one_or_none()


def get_person(family_name: str, first_name: str, birth_year: str, birth_place: str):
    # add table names we want to get back in the response
    return session.query(Person, Location).join(Location, and_(Location.locationPersonID == Person.personPersonID,
                                                               Person.TypeOfPerson == 1)
                                                ).outerjoin(
        TypeOfPerson,
        Person.TypeOfPerson == TypeOfPerson.PersonID
    ).filter(
        and_(Location.TypeOfLocation == 1,
             or_(
                 and_(
                     Person.FirstName.like(f'%{first_name}%'),
                     Person.LastName.like(f'%{family_name}%'),
                     or_(
                         func.extract('YEAR', Location.locationStartDate) == f'{birth_year}',
                         Location.locationStartDate is None
                     ),
                     or_(
                         Location.City == f'{birth_place}',
                         Location.City is None
                     )
                 ),
                 and_(
                     Person.LastName.like(f'%{family_name}%'),
                     func.extract('YEAR', Location.locationStartDate) == f'{birth_year}',
                     or_(
                         Location.City == f'{birth_place}',
                         Location.City is None
                     )
                 ),
                 and_(
                     Person.LastName.like(f'%{family_name}%'),
                     or_(
                         func.extract('YEAR', Location.locationStartDate) == f'{birth_year}',
                         Location.locationStartDate is None
                     ),
                     Location.City == f'{birth_place}'
                 )
             )
             )).one_or_none()


def get_education_count(person_id: int):
    return session.query(func.count(Education.EducationID)) \
        .filter(Education.personPersonID == person_id).scalar()


def get_particularity_count(person_id: int):
    return session.query(func.count(Particularity.ParticularityID)) \
        .filter(Particularity.personPersonID == person_id).scalar()


def get_career_count(person_id: int):
    return session.query(func.count(Career.CareerID)) \
        .filter(Career.personPersonID == person_id).scalar()


def update_person(person_ocr: schemas.Person, person_db: Person):
    if person_db is None:
        return None

    person_db.Faculty = person_ocr.faculty
    person_db.Rating = 2

    session.add(person_db)
    session.commit()
    session.refresh(person_db)
    return person_db


def update_education(person_ocr: schemas.Person, person_id: int):
    for education in person_ocr.education:
        response = Education(Subject=education.subject,
                             Location=education.location,
                             Date=education.date,
                             Source=education.source,
                             personPersonID=person_id)

        session.add(response)
        session.commit()
        session.refresh(response)
        print(f"Education {response.EducationID} added to education table for person {person_id}.")


def update_particularity(person_ocr: schemas.Person, person_id: int):
    for particularity in person_ocr.particularities:
        response = Particularity(Particularity=particularity.particularity,
                                 Location=particularity.location,
                                 Date=particularity.date,
                                 Source=particularity.source,
                                 personPersonID=person_id)

        session.add(response)
        session.commit()
        session.refresh(response)
        print(f"Particularity {response.ParticularityID} added to particularity table for person {person_id}.")


def update_career(person_ocr: schemas.Person, person_id: int):
    for career in person_ocr.careers:
        response = Career(Job=career.job,
                          Location=career.location,
                          Date=career.date,
                          Source=career.source,
                          IsSideJob=career.is_side_job,
                          personPersonID=person_id)

        session.add(response)
        session.commit()
        session.refresh(response)
        print(f"Career {response.CareerID} added to career table for person {person_id}.")


def create_location(person_id: int, date: str, type_of_location: int, city: str):
    db_location = Location(locationPersonID=person_id,
                           locationStartDate=date,
                           TypeOfLocation=type_of_location,
                           City=city)
    session.add(db_location)
    session.commit()
    session.refresh(db_location)
    print(f"Location {db_location.LocationID} added to location table for person {person_id}.")


def create_person(person: schemas.Person):
    db_user = Person(FirstName=person.FirstName,
                     LastName=person.LastName,
                     FamilyName=person.LastName,
                     Affix=person.Affix,
                     Nickname=person.alternative_last_names,
                     Gender=person.Gender,
                     Rating=1)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def create_relation(from_person_id: int, to_person_id: int, type_of_relation: int):
    db_relation = Relation(TypeOfRelation=type_of_relation,
                           FromPersonID=from_person_id,
                           ToPersonID=to_person_id)
    session.add(db_relation)
    session.commit()
    session.refresh(db_relation)
    print(f"Relation {db_relation.RelationID} added to relation table for person {from_person_id}.")
