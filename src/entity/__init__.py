from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import configs

Base = declarative_base()


def new_session():
    connection_string = f'mssql+pyodbc://{configs.SERVER}/{configs.DATABASE}?driver={configs.DRIVER}&trusted_connection=yes'
    engine = create_engine(connection_string)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
