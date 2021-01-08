import requests
import time
# import jmespath
from pprint import pprint

HOST = 'https://api.vk.com/method'
with open('vk_token.txt') as f:
    TOKEN = f.readline().strip().strip('\n')
MY_ID = '632744058'
MIKE_ID = '615929378'


# -------------------------------------------------------------------------------------------------

class VKuser:

    def __init__(self, user_id, first_name=None, last_name=None, is_closed=None, can_access_closed=None):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.is_closed = is_closed
        self.can_access_closed = can_access_closed

    def get_mutual_fiends(self, friend):
        if isinstance(friend, VKuser):
            method_name = '/friends.getMutual'
            params = {
                'source_uid': self.user_id,
                'target_uid': friend.user_id,
                'access_token': TOKEN,
                'v': '5.126'
            }
            r = requests.get(HOST + method_name, params=params)
            result = r.json()
        else:
            raise Exception('не верный тип аргумента')
        return result['response']

    def get_user_info(self, user_id):
        method_name = '/users.get'
        params = {
            'user_id': user_id,
            'access_token': TOKEN,
            'fields': 'first_name, last_name',
            'v': '5.126'
        }
        r = requests.get(HOST + method_name, params=params)
        result = r.json()
        return result['response'][0]

    def __and__(self, user):
        if isinstance(user, VKuser):
            mutual_fiends_list = []
            mutual_fiends = self.get_mutual_fiends(user)
            for i, el in enumerate(mutual_fiends):
                user = self.get_user_info(el)
                user_id = user['id']
                first_name = user['first_name']
                last_name = user['last_name']
                is_closed = user['is_closed']
                can_access_closed = user['can_access_closed']
                mutual_fiends_list.append(VKuser(user_id, first_name, last_name, is_closed,can_access_closed))
                time.sleep(1)
        else:
            raise Exception('не верный тип аргумента')
        return mutual_fiends_list

    def __str__(self):
        url = f'https://vk.com/id{self.user_id}'
        return url


# -------------------------------------------------------------------------------------------------

vk_user_1 = VKuser(MY_ID)
print(vk_user_1)

vk_user_2 = VKuser(MIKE_ID)
print(vk_user_2)

print()
print(vk_user_1.get_mutual_fiends(vk_user_2))

mutual_fiends = vk_user_1 & vk_user_2
print(mutual_fiends)

for obj in mutual_fiends:
    print(obj)