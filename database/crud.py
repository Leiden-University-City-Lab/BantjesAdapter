from sqlalchemy import and_
from database import Session
from . import models, schemas

session = Session()


def get_person(family_name: str, first_name: str):
    return session.query(models.Person).filter(
        and_(models.Person.FamilyName.contains(family_name),
             models.Person.FirstName.contains(first_name))).first()


def create_person(person: schemas.Person):
    db_user = models.Person(FirstName=person.FirstName,
                            LastName=person.FamilyName,
                            FamilyName=person.FamilyName)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
