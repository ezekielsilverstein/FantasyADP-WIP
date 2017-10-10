import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from models import Base

db_string = 'postgresql://ezekielsilverstein:Maccabee@localhost:5432/adp'
db = sqlalchemy.create_engine(db_string, client_encoding='utf8')
if not database_exists(db.url):
    create_database(db.url)

Session = sessionmaker(db)
session = Session()

Base.metadata.create_all(db)
