from sqlalchemy import and_, or_, func, update
from database import Session
from .models import Person, Location, TypeOfPerson, Relation, TypeOfRelation, Education, Particularity, \
    Career, TypeOfLocation
from . import schemas

session = Session()


def get_person(family_name: str, first_name: str, birth_year: str, birth_place: str):
    # add table names we want to get back in the response
    return session.query(Person,
                         TypeOfPerson,
                         Relation,
                         TypeOfRelation,
                         Location,
                         TypeOfLocation,
                         Particularity,
                         Education,
                         Career).join(
        Location,
        and_(Location.locationPersonID == Person.personPersonID,
             Person.TypeOfPerson == 1
             )).outerjoin(
        Relation,
        Relation.FromPersonID == Person.personPersonID
    ).outerjoin(
        TypeOfLocation,
        Location.TypeOfLocation == TypeOfLocation.LocationID
    ).outerjoin(
        TypeOfRelation,
        Relation.RelationID == TypeOfRelation.RelationID
    ).outerjoin(
        Education,
        Person.personPersonID == Education.personPersonID
    ).outerjoin(
        Career,
        Person.personPersonID == Career.personPersonID
    ).outerjoin(
        TypeOfPerson,
        Person.TypeOfPerson == TypeOfPerson.PersonID
    ).outerjoin(
        Particularity,
        Person.personPersonID == Particularity.personPersonID
    ).filter(
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
    ).all()


def update_person(person_ocr: schemas.Person, person_db: Person):

    if person_db is None:
        return None

    person_db.Faculty = person_ocr.faculty
    person_db.Rating = 2

    session.add(person_db)
    session.commit()
    session.refresh(person_db)
    return person_db


def update_education(education_ocr: schemas.Education, education_db: Education, person_id: int):
    if education_db is None:
        return None

    for education in education_ocr:
        education_db.personPersonID = person_id
        education_db.Subject = education.subject
        education_db.Location = education.location
        education_db.Date = education.date
        education_db.Source = education.source

        session.add(education_db)
        session.commit()
        session.refresh(education_db)


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
