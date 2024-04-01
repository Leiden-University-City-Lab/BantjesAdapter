from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from .models import Base

engine = create_engine('mysql://root@localhost:3306')
Session = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)
