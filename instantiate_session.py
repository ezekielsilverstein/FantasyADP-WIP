import configparser
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from models import Base

config = configparser.ConfigParser()
config.read('config.ini')
username = config['DEFAULT']['username']
password = config['DEFAULT']['password']

db_string = 'postgresql://{}:{}@localhost:5432/redraft_adp'.format(username, password)
db = sqlalchemy.create_engine(db_string, client_encoding='utf8')
if not database_exists(db.url):
    create_database(db.url)

Session = sessionmaker(db)
session = Session()

Base.metadata.create_all(db)
