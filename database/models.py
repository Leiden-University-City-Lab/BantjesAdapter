from sqlalchemy import Column, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'
    __table_args__ = {'schema': 'univercity'}
    personPersonID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String(50))
    LastName = Column(String(50))
    FamilyName = Column(String(50))
    Affix = Column(String(45))
    Nickname = Column(String(50))
    Gender = Column(String(45))
    TypeOfPerson = Column(Integer, ForeignKey('univercity.type_of_person.PersonID'))
    BirthDate = Column(String(50))
    BirthYear = Column(String(50))
    BirthCountry = Column(String(50))
    BirthCity = Column(String(50))
    BaptizedDate = Column(String(50))
    DeathDate = Column(String(50))
    DeathCity = Column(String(50))
    DeathCountry = Column(String(50))
    Faculty = Column(String(50))
    Rating = Column(Integer)


class Education(Base):
    __tablename__ = 'education'
    __table_args__ = {'schema': 'univercity'}
    EducationID = Column(Integer, primary_key=True, autoincrement=True)
    personPersonID = Column(Integer, ForeignKey('univercity.person.personPersonID'))
    Subject = Column(String(100))
    Location = Column(String(50))
    Date = Column(String(50))
    Source = Column(String(50))


class Career(Base):
    __tablename__ = 'career'
    __table_args__ = {'schema': 'univercity'}
    CareerID = Column(Integer, primary_key=True, autoincrement=True)
    personPersonID = Column(Integer, ForeignKey('univercity.person.personPersonID'))
    Job = Column(String(500))
    Location = Column(String(50))
    Date = Column(String(50))
    Source = Column(String(50))
    IsSideJob = Column(Boolean, default=False)


class Particularity(Base):
    __tablename__ = 'particularity'
    __table_args__ = {'schema': 'univercity'}
    ParticularityID = Column(Integer, primary_key=True, autoincrement=True)
    personPersonID = Column(Integer, ForeignKey('univercity.person.personPersonID'))
    Particularity = Column(String(500))
    Location = Column(String(50))
    Date = Column(String(50))
    Source = Column(String(50))


class Family(Base):
    __tablename__ = 'family'
    __table_args__ = {'schema': 'univercity'}
    FamilyID = Column(Integer, primary_key=True, autoincrement=True)
    FirstName = Column(String(50))
    LastName = Column(String(50))
    BirthPlace = Column(String(50))
    BaptizedDate = Column(String(50))
    DeathDate = Column(String(50))
    DeathPlace = Column(String(50))
    Source = Column(String(50))


class Relation(Base):
    __tablename__ = 'relation'
    __table_args__ = {'schema': 'univercity'}
    RelationID = Column(Integer, primary_key=True, autoincrement=True)
    TypeOfRelation = Column(Integer, ForeignKey('univercity.type_of_relation.RelationID'))
    FromPersonID = Column(Integer, ForeignKey('univercity.person.personPersonID'))
    ToPersonID = Column(Integer, ForeignKey('univercity.person.personPersonID'))
    ToFamilyID = Column(Integer, ForeignKey('univercity.family.FamilyID'))


class TypeOfRelation(Base):
    __tablename__ = 'type_of_relation'
    __table_args__ = {'schema': 'univercity'}
    RelationID = Column(Integer, primary_key=True, autoincrement=True)
    RelationType = Column(String(100), nullable=False)


class PersonSource(Base):
    __tablename__ = 'person_source'
    __table_args__ = {'schema': 'univercity'}
    PersonID = Column(Integer, primary_key=True)


class Location(Base):
    __tablename__ = 'location'
    __table_args__ = {'schema': 'univercity'}
    LocationID = Column(Integer, primary_key=True, autoincrement=True)
    TypeOfLocation = Column(Integer, ForeignKey('univercity.type_of_location.LocationID'))
    locationPersonID = Column(Integer, ForeignKey('univercity.person.personPersonID'))
    Country = Column(String(100))
    City = Column(String(100))
    Street = Column(String(100))
    HouseNumber = Column(String(10))
    Region = Column(String(100))
    locationStartDate = Column(String(20))
    locationEndDate = Column(String(20))


# class Location(Base):
#     __tablename__ = 'location'
#     __table_args__ = {'schema': 'univercity'}
#     LocationID = Column(Integer, primary_key=True)
#     locationPersonID = Column(Integer, ForeignKey('univercity.person.personPersonID'))
#     TypeOfLocation = Column(Integer, ForeignKey('univercity.type_of_location.LocationID'))
#     locationStartDate = Column(String(20))
#     City = Column(String(100))
#
#
# class TypeOfLocation(Base):
#     __tablename__ = 'type_of_location'
#     __table_args__ = {'schema': 'univercity'}
#     LocationID = Column(Integer, primary_key=True)
#     LocationType = Column(String(100))
#
#
class TypeOfPerson(Base):
    __tablename__ = 'type_of_person'
    __table_args__ = {'schema': 'univercity'}
    PersonID = Column(Integer, primary_key=True)
    PersonType = Column(String(100))


# class Miscellaneous(Base):
#     __tablename__ = 'miscellaneous'
#     __table_args__ = {'schema': 'univercity'}
#     miscellaneousID = Column(Integer, primary_key=True)
#     personID = Column(Integer, ForeignKey('univercity.person.personPersonID'))
#     description = Column(String(500), nullable=False)
    # sourceID = Column(Integer, ForeignKey('type_of_source.sourceID'))
    # date = Column(DateTime, default=datetime.utcnow)
    # sources = relationship('type_of_source_banjers', secondary=Association_table, back_populates='Miscellaneous')
    # Define the relationship with Person
    # person = relationship('Person1', back_populates='misc_items')


# class TypeOfSource(Base):
#     __tablename__ = 'type_of_source'
#     __table_args__ = {'schema': 'univercity'}
#     SourceID = Column(Integer, primary_key=True)
#     SourceType = Column(String(100))
#     Rating = Column(Integer)
