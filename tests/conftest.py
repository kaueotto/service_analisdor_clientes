import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.entity.orm import Base


@pytest.fixture(scope='session')
def engine():
    return create_engine('sqlite:///:memory:')


@pytest.fixture(scope='session')
def setup_database(engine):
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def session(engine, setup_database):
    Session = sessionmaker(bind=engine)
    return Session()
