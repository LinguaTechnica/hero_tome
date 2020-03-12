from flask_sqlalchemy import SQLAlchemy

from werkzeug.security import generate_password_hash, check_password_hash

# from sqlalchemy import create_engine
# from sqlalchemy.orm import scoped_session, sessionmaker
# from sqlalchemy.schema import Table
# from sqlalchemy.ext.declarative import declarative_base
#
# engine = create_engine('postgres:///herotome', echo=False)
# db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
#
# db = declarative_base()
# db.query = db_session.query_property()

db = SQLAlchemy()

# Users' favorite heroes
favorites_table = db.Table('favorites',
                           db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
                           db.Column('hero_id', db.Integer, db.ForeignKey('heroes.id')))


class ModelMixin:
    def save(self):
        db.session.add(self)
        db.session.commit()


class User(ModelMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(75), nullable=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String, nullable=False)
    favorites = db.relationship('Hero', secondary='favorites')

    def __repr__(self):
        return f'<User {self.id} | {self.username}>'

    def create_password(self, password):
        self.password = generate_password_hash(password)

    def login(self, password):
        return check_password_hash(self.password, password)

    def is_valid_password(self, password):
        return self.login(self.password, password)


class Hero(ModelMixin, db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    alignment = db.Column(db.String)
    race = db.Column(db.String)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    power = db.Column(db.Integer)
    durability = db.Column(db.Integer)
    combat = db.Column(db.Integer)
    speed = db.Column(db.Integer)


def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///herotome'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    # from flask import Flask
    # app = Flask(__name__)
    #
    # connect_to_db(app)
    # db.create_all()

    print('Connected to database, tables ready.')
