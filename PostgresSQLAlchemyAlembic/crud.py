# we create an engine using the connection string. To create an engine we use SQA's create_engine
from contextlib import contextmanager
from datetime import datetime

from sqlalchemy import create_engine
# make a session
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URI
from models import Base, Student, Admin
import yaml

engine = create_engine(DATABASE_URI)

Session = sessionmaker(bind=engine)
s = Session()


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def recreate_database():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def load_yaml():
    with session_scope() as s:
        for data in yaml.load_all(open('students.yaml'), Loader=yaml.FullLoader):
            book = Student(**data)
            s.add(book)
        for data in yaml.load_all(open('admins.yaml'), Loader=yaml.FullLoader):
            book = Admin(**data)
            s.add(book)

# def load_admin_yaml():
#     with session_scope() as s:
#         for data in yaml.load_all(open('admins.yaml'), Loader=yaml.FullLoader):
#             book = Admin(**data)
#             s.add(book)

recreate_database()
    # add_data()
    # load_yaml()
