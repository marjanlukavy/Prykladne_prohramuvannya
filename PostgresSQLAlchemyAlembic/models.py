from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import MONEY
from sqlalchemy.orm import relationship

Base = declarative_base()


# успадкування Base для реєстрації моделей у SQA.
class Admin(Base):
    __tablename__ = 'admins'  # table name
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    right = Column(Boolean)
    def __repr__(self):
        return "<Student(first_name='{}', last_name='{}', right={})>" \
            .format(self.first_name, self.last_name, self.right)
class Student(Base):
    __tablename__ = 'students'  # table name
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    student_rating = Column(Integer)
    right = Column(Boolean)
    published = Column(Date)
    admin_id = Column(Integer, ForeignKey('admins.id'))
    students = relationship(Admin, backref="students", lazy="joined")

    def __repr__(self):
        return "<Student(first_name='{}', last_name='{}', student_rating={}, published={})>" \
            .format(self.first_name, self.last_name, self.student_rating, self.published)

