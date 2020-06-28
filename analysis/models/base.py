from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from config import CONFIG


DEBUG = False
engine = create_engine(f'sqlite:///{CONFIG["PROJECT_DIR"]}/db.sqlite', echo=DEBUG)
Session = sessionmaker()
Session.configure(bind=engine)
session = Session()


class _Base:
    @declared_attr
    def __tablename__(cls):  # pylint: disable=no-self-argument
        return cls.__name__.lower()  # pylint: disable=no-member


Base = declarative_base(cls=_Base)
