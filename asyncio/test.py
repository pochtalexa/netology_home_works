import requests
from pprint import pprint

BASE_URL = 'https://swapi.dev/api/'

# r = requests.get(BASE_URL + 'people/')
# r = requests.get(BASE_URL + 'people/?page=9')
r = requests.get(BASE_URL + 'people/17/')

result = r.json()

pprint(result)

