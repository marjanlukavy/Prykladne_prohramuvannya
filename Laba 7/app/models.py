from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

admins_have_students = db.Table('admins_have_students',
                                db.Column('admin_id', db.Integer, db.ForeignKey('admins.id'), primary_key=True),
                                db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True))

admins_id = db.Table('admins_id',
                     db.Column('admin_id', db.Integer, db.ForeignKey('admins.id'), primary_key=True),
                     db.Column('student_id', db.Integer, db.ForeignKey('students.id'), primary_key=True))


class User(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    rating = db.Column(db.Integer)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    # bucketlists = db.relationship(
    #     'Admin', order_by='Admin.id', cascade="all, delete-orphan")
    admins_students = db.relationship('Admin', secondary=admins_id, lazy="subquery",
                                      backref=db.backref('admins_id', lazy=True))

    def __init__(self, email, password, first_name, last_name, rating):
        self.first_name = first_name
        self.last_name = last_name
        self.rating = rating
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    # def password_is_valid(self, password):
    #
    #     return Bcrypt().check_password_hash(self.password, password)

    @staticmethod
    def get_all():
        return User.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()


class Admin(db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))
    admins_have_students = db.relationship('User', secondary=admins_have_students, lazy="subquery",
                                      backref=db.backref('admins_have_students', lazy=True))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Admin.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Admin: {}>".format(self.name)
