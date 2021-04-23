from netology.diplom_VKfinder.vk_api import users_get, users_search, get_user_photos, get_top_3_photos, get_offset
from pprint import pprint
import datetime
import time

if __name__ == '__main__':
    now = datetime.datetime.now()
    now_year = now.year

    # user_id = 'elenabykhanova'
    # user_id = '25835887'
    # user_id = '490361025'
    # user_id = '47030363'

    user_info = users_get()
    # pprint(user_info)

    age = now_year - int(user_info['byear'].split('.')[2])
    sex = user_info['sex']
    city_id = user_info['city_id']
    status = user_info['status']
    user_id = user_info['user_id']

    offset = get_offset(user_id, age, sex, city_id, status)
    users = users_search(age, sex, city_id, status, offset)
    # pprint(users)

    for user in users:
        user_id = user['id']
        user_photos = get_user_photos(user_id)

        time.sleep(0.5)

        top_3_photos = get_top_3_photos(user_photos, user_id)
        pprint(top_3_photos)
        print()
