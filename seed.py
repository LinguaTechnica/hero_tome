import json

from models import *

# Seed Files
HERO_INFO = 'data/hero_info.json'
HERO_POWERS = 'data/hero_powers.json'
HERO_STATS = 'data/hero_stats.json'


def seed():
    with open(HERO_INFO) as f:
        hero_info = json.load(f)

    for hero in hero_info:
        key_data = {k.lower(): v for k, v in hero.items()}
        hero_keys = key_data.keys() & dir(Hero)

        data = {k: key_data[k]for k in hero_keys}
        print(data)


