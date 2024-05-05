from sqlalchemy.sql import and_, or_, func
from database import Session
from . import models, schemas

session = Session()


def get_person(family_name: str, first_name: str, birth_year: str, birth_place: str):
    # add table names we want to get back in the response
    return session.query(models.Person, models.TypeOfPerson).join(
        models.Location,
        and_(models.Location.locationPersonID == models.Person.personPersonID,
             models.Person.TypeOfPerson == 1
             )).outerjoin(
        models.Relation,
        models.Relation.FromPersonID == models.Person.personPersonID
    ).outerjoin(
        models.TypeOfRelation,
        models.Relation.RelationID == models.TypeOfRelation.RelationID
    ).outerjoin(
        models.Family,
        models.Relation.ToFamilyID == models.Family.FamilyID
    ).outerjoin(
        models.Education,
        models.Person.personPersonID == models.Education.personPersonID
    ).outerjoin(
        models.Career,
        models.Person.personPersonID == models.Career.personPersonID
    ).outerjoin(
        models.TypeOfPerson,
        models.Person.TypeOfPerson == models.TypeOfPerson.PersonID
    ).outerjoin(
        models.Particularity,
        models.Person.personPersonID == models.Particularity.personPersonID
    ).filter(
        or_(
            and_(
                models.Person.FirstName.like(f'%{first_name}%'),
                models.Person.LastName.like(f'%{family_name}%'),
                or_(
                    func.extract('YEAR', models.Location.locationStartDate) == f'{birth_year}',
                    models.Location.locationStartDate is None
                ),
                or_(
                    models.Location.City == f'{birth_place}',
                    models.Location.City is None
                )
            ),
            and_(
                models.Person.LastName.like(f'%{family_name}%'),
                func.extract('YEAR', models.Location.locationStartDate) == f'{birth_year}',
                or_(
                    models.Location.City == f'{birth_place}',
                    models.Location.City is None
                )
            ),
            and_(
                models.Person.LastName.like(f'%{family_name}%'),
                or_(
                    func.extract('YEAR', models.Location.locationStartDate) == f'{birth_year}',
                    models.Location.locationStartDate is None
                ),
                models.Location.City == f'{birth_place}'
            )
        )
    ).one()


def update_person():
    return ''

# def get_birth_year():
#     return session.query(
#         func.extract('YEAR', models.Location.locationStartDate).label("Birth year"),
#     ).join(
#         models.Person,
#         and_(models.Person.personPersonID == models.Location.locationPersonID, models.Person.type_of_person == 1)
#     ).filter(
#         models.Location.TypeOfLocation == 1,
#         models.Location.locationStartDate is not None
#     )


def create_person(person: schemas.Person):
    db_user = models.Person(FirstName=person.first_name,
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
