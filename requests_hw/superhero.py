import requests
from pprint import pprint

TOKEN = '2619421814940190/'
HOST = 'https://superheroapi.com/api/' + TOKEN
HEROES = ['Hulk', 'Captain America', 'Thanos']


# --------------------------------------------------------------------------------------------------
def get_superhero_intelligence(name):
    r = requests.get(HOST + '/search/' + f'{name}')
    result = r.json()

    for el in result['results']:
        if el['name'] == name:
            intelligence = el['powerstats']['intelligence']
    # print(name, intelligence)
    return intelligence


def get_best_hero(heroes):
    intelligence = 0
    best_hero = ''
    for hero in heroes:
        hero_intelligence = get_superhero_intelligence(hero)
        if int(hero_intelligence) > intelligence:
            intelligence = int(hero_intelligence)
            best_hero = hero
    return best_hero


# --------------------------------------------------------------------------------------------------

best_hero = get_best_hero(HEROES)
print(best_hero)
