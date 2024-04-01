from database import Session
from database.models import Person

session = Session()


def query_person():
    person = session.query(Person).filter(Person.personPersonID == 3).first()
    return person.FirstName


# for u in session.query(Person) \
#         .join(Type_of_person, Type_of_person.PersonID == Person.TypeOfPerson) \
#         .filter(Person.LastName.like('%Aalst%')) \
#         .with_entities(Type_of_person.PersonType, Person.FirstName) \
#         .all():
#     print(u)
#     row_as_dict = u._mapping
#
# print(row_as_dict)

# join location and type_of_location

# stmt = select(Location.City, Type_of_location.LocationType).select_from(
#     Location).join(Type_of_location, Location.TypeOfLocation == Type_of_location.LocationID)
#
# results = session.execute(stmt)
#
# for row in results:
#     print(row)

# join person and location
# stmt = select(Location.City, Person.LastName).select_from(
#     Person, Location).join(Person, Location.TypeOfLocation == Person.personPersonID)

# stmt1 = stmt.filter(
#     Person.LastName == 'Aalst')

# results = session.execute(stmt)
#
# for row in results:
#     print(row)


# for _row in query.all():
#     print(_row.FirstName, _row.LastName, _row.locationStartDate, _row.City)

# _row = query.first()
# print(_row.FirstName)
