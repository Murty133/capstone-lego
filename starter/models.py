import os
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Lego Collections

'''
collection = db.Table(
    'collection',
    Column('collector_id', Integer, ForeignKey(
        'collectors.id'), primary_key=True),
    Column('set_id', Integer, ForeignKey('sets.id'), primary_key=True)
    )

'''
Extend the base Model class to add common methods

'''


class CommonHelperMethods(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def rollback(self):
        db.session.rollback()


'''
Collectors

'''


class Collector(CommonHelperMethods):
    __tablename__ = 'collectors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    legos = db.relationship(
        'Set', secondary=collection,
        backref=db.backref('collectors', lazy=True))

    def __init__(self, name, location, legos):
        self.name = name
        self.location = location
        self.legos = legos

    def short(self):
        return {
            'name': self.name,
            'location': self.location
            }

    def long(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'sets collected': [lego.id for lego in self.legos]
            }


'''
Lego Sets

'''


class Set(CommonHelperMethods):
    __tablename__ = 'sets'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    year = Column(String, nullable=False)
    pieces = Column(Integer, nullable=False)

    def __init__(self, id, name, year, pieces):
        self.id = id
        self.name = name
        self.year = year
        self.pieces = pieces

    def short(self):
        return {
            'set number': self.id,
            'name': self.name,
            'release year': self.year,
            'number of pieces': self.pieces
            }

    def long(self):
        return {
            'set number': self.id,
            'name': self.name,
            'release year': self.year,
            'number of pieces': self.pieces,
            'collectors': [collector.name for collector in self.collectors]
        }
