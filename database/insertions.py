# data = {'a': 'test', 'b': 'test2'}
# try:
#     for _key, _val in data.items():
#         row = TestTable(key=_key, val=_val)
#         session.add(row)
#     session.commit()
# except SQLAlchemyError as e:
#     print(e)
# finally:
#     session.close()


# # drop tables
# # Miscellaneous.__table__.drop(engine)
# # Type_of_source_test.__table__.drop(engine)
