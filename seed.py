import json

from models import *

# Seed Files
HERO_INFO = 'data/hero_info.json'
HERO_POWERS = 'data/hero_powers.json'
HERO_STATS = 'data/hero_stats.json'


def create_heroes():
    """Seeds database with basic Hero info."""
    with open(HERO_INFO) as f:
        hero_info = json.load(f)

    for hero in hero_info:
        key_data = {k.lower(): v for k, v in hero.items()}
        hero_keys = key_data.keys() & dir(Hero)
        hero_keys.remove('id')

        data = {k: key_data[k]for k in hero_keys}

        # Convert '-' to None.
        remove_dashes(data)
        create_hero(data)

        print(f'{data}')
    print('Seeding complete. Enjoy your heroes!')


def add_stats():

    def update(hero_data):
        if 'total' in hero_data:
            del hero_data['total']
        hero = Hero.query.filter_by(name=hero_data['Name']).first()
        if hero:
            for attr in hero_data:
                if attr in dir(Hero):
                    setattr(hero, attr.lower(), hero_data[attr])
            hero.save()

    with open(HERO_POWERS) as f:
        hero_info = json.load(f)

    for data in hero_info:
        update(data)


def remove_dashes(data):
    for k, v in data.items():
        if v == '-':
            data[k] = None


def create_hero(data):
    hero = Hero(**data)
    hero.save()
    return hero


if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    # Clear out the DB and recreate
    db.reflect()
    db.drop_all()
    db.create_all()

    print('Connected to database, tables ready.')
