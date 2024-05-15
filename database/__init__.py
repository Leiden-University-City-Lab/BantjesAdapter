from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('mysql://root@localhost:3306')
Session = sessionmaker(bind=engine)

Base = automap_base()
Base.prepare(autoload_with=engine, schema="univercity")
