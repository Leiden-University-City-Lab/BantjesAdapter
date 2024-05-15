from sqlalchemy import and_, or_, func, update
from database import Session
from .models import Person, Location, TypeOfPerson, Relation, TypeOfRelation, Education, Particularity, \
    Career, TypeOfLocation
from . import schemas

session = Session()


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
    return session.query(func.count(Education.EducationID))\
        .filter(Education.personPersonID == person_id).scalar()


def get_particularity_count(person_id: int):
    return session.query(func.count(Particularity.ParticularityID))\
        .filter(Particularity.personPersonID == person_id).scalar()


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
        print(response)


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
        print(response)


# def get_birth_year():
#     return session.query(
#         func.extract('YEAR', Location.locationStartDate).label("Birth year"),
#     ).join(
#         Person,
#         and_(Person.personPersonID == Location.locationPersonID, Person.type_of_person == 1)
#     ).filter(
#         Location.TypeOfLocation == 1,
#         Location.locationStartDate is not None
#     )


def create_person(person: schemas.Person):
    db_user = Person(FirstName=person.first_name,
                     LastName=person.last_name,
                     FamilyName=person.last_name,
                     Affix=person.affix,
                     Nickname=person.alternative_last_names,
                     Gender=person.gender,
                     TypeOfPerson=person.type_of_person,
                     BirthDate=person.birth_date,
                     BirthCountry=person.birth_country,
                     BirthCity=person.birth_city,
                     BaptizedDate=person.baptized_date,
                     DeathDate=person.death_date,
                     DeathCity=person.death_city,
                     DeathCountry=person.death_country,
                     Faculty=person.faculty)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
