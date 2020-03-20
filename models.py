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
    # TODO: More utility methods like .get()!

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

    def serialize(self):
        return {
            "id": self.id, "username": self.username,
            "email": self.email,
            "favorites": [fav.serialize() for fav in self.favorites]
        }

    def create_password(self, password):
        self.password = generate_password_hash(password)

    def is_valid_password(self, password):
        check_password_hash(self.password, password)


class Hero(ModelMixin, db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    alignment = db.Column(db.String)
    race = db.Column(db.String)
    height = db.Column(db.String)
    weight = db.Column(db.String)
    intelligence = db.Column(db.String)
    strength = db.Column(db.String)
    power = db.Column(db.String)
    durability = db.Column(db.String)
    combat = db.Column(db.String)
    speed = db.Column(db.String)

    def __repr__(self):
        return f'<Hero {self.id} | {self.name }>'

    def serialize(self):
        return {
            'name': self.name, 'alignment': self.alignment, 'race': self.race,
            'height': self.height, 'weight': self.weight, 'intelligence': self.intelligence,
            'strength': self.strength, 'power': self.power, 'durability': self.durability,
            'combat': self.combat, 'speed': self.speed
        }


def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///herotome'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    db.create_all()

    print('Connected to database, tables ready.')
