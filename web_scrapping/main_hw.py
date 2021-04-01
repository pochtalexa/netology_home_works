import requests
from bs4 import BeautifulSoup
import re

# определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']

URL = 'https://habr.com/ru/all/'


def find_key_words(input_el: str):
    input_el = input_el.lower().strip()
    input_el = re.sub('r[\r\n]+', '', input_el)

    for key_word in KEYWORDS:
        if input_el.find(key_word) != -1:
            return 1
    return 0


if __name__ == '__main__':

    pattern_1 = re.compile(r'^post_\d+$')
    pattern_2 = re.compile(r'^post__text.+$')

    r = requests.get(URL)
    soap = BeautifulSoup(r.text, 'html.parser')
    posts = soap.find_all('li', id=pattern_1)

    for post in posts:
        post_date = post.find('span', class_=re.compile(r'preview-data__time-published|post__time')).text

        try:
            post_link = post.find('a', class_='post__user-info user-info').get('href')
        except Exception as e:
            post_link = ''

        try:
            h2 = [post.find('h2', class_='post__title').text.strip()]
        except Exception as e:
            h2 = []

        hubs = [hub.text.strip().replace(',', '') for hub in
                post.find_all('li', class_='inline-list__item inline-list__item_hub')]

        try:
            text_post = [post.find(class_=re.compile(r'post__text.+')).text]
        except Exception as e:
            text_post = []

        if sum(list(map(find_key_words, h2 + hubs + text_post))):
            print(f'{post_date} - {"".join(h2)} - {post_link}')