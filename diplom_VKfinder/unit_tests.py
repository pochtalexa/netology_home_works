from netology.diplom_VKfinder.vk_api import users_get, users_search, get_user_photos, get_top_3_photos, get_offset
from unittest.mock import patch
import datetime
from pprint import pprint


class TestClass:

    @patch('builtins.input', side_effect=['1980', '5'])
    def test_users_get_11(self, mock_input):
        user_id = '25835887'
        user_info = users_get(user_id)
        assert user_info['status'] == 5

    def test_offset_11(self):
        age = '0'
        sex = '0'
        city_id = '0'
        status = '0'
        user_id = '0'
        offset = get_offset(user_id, age, sex, city_id, status)
        assert not offset is None

    def test_users_search_11(self):
        now = datetime.datetime.now()
        now_year = now.year
        user_id = 'elenabykhanova'
        user_info = users_get(user_id)
        age = now_year - int(user_info['byear'].split('.')[2])
        sex = user_info['sex']
        city_id = user_info['city_id']
        status = user_info['status']
        user_id = user_info['user_id']
        offset = 10
        users = users_search(age, sex, city_id, status, offset)
        assert len(users) > 0

    def test_get_user_photos_11(self):
        user_id = '9875988'
        user_photos = get_user_photos(user_id)
        assert len(user_photos) > 0

    def test_get_top_3_photos_11(self):
        user_id = '9875988'
        user_photos = get_user_photos(user_id)
        top_3_photos = get_top_3_photos(user_photos, user_id)
        assert len(top_3_photos) > 0





