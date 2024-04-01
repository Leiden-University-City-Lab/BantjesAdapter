from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Person(Base):
    __tablename__ = 'person'
    __table_args__ = {'schema': 'univercity'}
    personPersonID = Column(Integer, primary_key=True)
    FirstName = Column(String(50))
    LastName = Column(String(50))
    TypeOfPerson = Column(Integer, ForeignKey('univercity.type_of_person.PersonID'))


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


class Miscellaneous(Base):
    __tablename__ = 'miscellaneous'
    __table_args__ = {'schema': 'univercity'}
    miscellaneousID = Column(Integer, primary_key=True)
    personID = Column(Integer, ForeignKey('univercity.person.personPersonID'))
    description = Column(String(500), nullable=False)
    # sourceID = Column(Integer, ForeignKey('type_of_source.sourceID'))
    date = Column(DateTime, default=datetime.utcnow)
    # sources = relationship('type_of_source_banjers', secondary=Association_table, back_populates='Miscellaneous')
    # Define the relationship with Person
    # person = relationship('Person1', back_populates='misc_items')


# class TypeOfSource(Base):
#     __tablename__ = 'type_of_source'
#     __table_args__ = {'schema': 'univercity'}
#     SourceID = Column(Integer, primary_key=True)
#     SourceType = Column(String(100))
#     Rating = Column(Integer)
