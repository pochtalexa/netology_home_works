import requests
import pandas as pd
import jmespath
import datetime
import sqlalchemy
import json

# -------------------------------------------------------------------------------------------------
# отображать все колонки
pd.set_option('display.max_columns', 30)
pd.set_option("max_colwidth", 50)

HOST = 'https://api.vk.com/method'

with open('vk_token.txt') as f:
    TOKEN = f.readline().strip().strip('\n')

with open("db_credentials.json") as f:
    db_credentials = json.load(f)

db = f"postgresql://{db_credentials['username']}:{db_credentials['password']}@localhost:5432/{db_credentials['db_name']}"
engine = sqlalchemy.create_engine(db)
connection = engine.connect()


# -------------------------------------------------------------------------------------------------
def get_offset(user_id, age, sex, city_id, status):

    def select():
        select = f'''
        select a.offset from users_search as a
        where a.user_id={user_id}     
        and a.age={age}
        and a.sex={sex}
        and a.city_id={city_id}
        and a.status={status};
        '''
        return select

    def insert():
        insert = f'''
        INSERT INTO users_search (user_id, age, sex, city_id, status, "offset") 
        VALUES ({user_id}, {age}, {sex}, {city_id}, {status}, {new_offset});
        '''
        return insert

    def update():
        update = f'''
        UPDATE users_search SET
        "offset" = {new_offset}
        WHERE user_id = {user_id}
          and age = {age}
          and sex = {sex} 
          and city_id = {city_id} 
          and status = {status};
        '''
        return update

    offset = connection.execute(select()).fetchone()

    if not offset is None:
        offset = offset[0]

    if offset is None:
        offset = 0
        new_offset = offset + 10
        sql_res = connection.execute(insert())
    elif 1 <= offset <= 1200:
        new_offset = offset + 10
        sql_res = connection.execute(update())
    else:
        raise Exception(f'there are no new results for user_id - {user_id}')

    return offset


def users_search(age: int, sex, city_id, status, offset):
    method_name = '/users.search'
    params = {
        'access_token': TOKEN,
        'v': '5.126',
        'fields': 'city,sex',
        'age_from': age,
        'age_to': age,
        'sex': sex,
        'city': city_id,
        'status': status,
        'sort': 0,
        'count': 10,
        'offset': offset
    }

    r = requests.get(HOST + method_name, params=params)
    r.raise_for_status()
    result = r.json()

    if result.get('error'):
        error_code = result['error']['error_code']
        error_msg = result['error']['error_msg']
        raise Exception('api error:', error_code, error_msg)
    elif result.get('response').get('count') == 0:
        raise Exception('there are no requests for your request')

    return result['response']['items']


def get_user_photos(user_id):
    method_name = '/photos.get'
    params = {
        'access_token': TOKEN,
        'v': '5.126',
        'owner_id': user_id,
        'album_id': 'profile',
        'extended': 1,
        'photo_sizes': 1
    }
    r = requests.get(HOST + method_name, params=params)
    r.raise_for_status()
    result = r.json()

    try:
        return result['response']['items']
    except KeyError:
        return None


def get_top_3_photos(user_photos, user_id):
    df_result = pd.DataFrame()

    # no photos
    if user_photos is None or user_photos == []:
        df_result.loc[0, 'user_id'] = user_id
        df_result.loc[0, 'link'] = f'https://vk.com/id{user_id}'
        df_result.loc[0, 'url'] = None

        df_result['user_id'] = df_result['user_id'].astype('int')

        sql_save_res = df_result[['user_id', 'link', 'url']].to_sql('search_results', con=connection, index=False,
                                                                    if_exists='append')

        result = df_result[['user_id', 'link', 'url']].to_dict('records')
        return result

    def get_max_resolution_id():
        max_res = 0
        max_res_id = None
        for i, el in enumerate(heights):
            if el > max_res:
                max_res = el
                max_res_id = i
        if max_res_id is None:
            return 0
        else:
            return max_res_id

    def get_top_photos(df_in):
        result = df_in.sort_values(by='rating', ascending=False).reset_index(drop=True).loc[0:2]
        return result

    for el in user_photos:

        # if user_id == '163811926':
        if user_id == 164626052:
            print('---el---', el)

        df_temp = pd.DataFrame()
        heights = jmespath.search('sizes[*].height', el)
        widths = jmespath.search('sizes[*].width', el)
        ph_types = jmespath.search('sizes[*].type', el)
        urls = jmespath.search('sizes[*].url', el)
        user_likes = jmespath.search('likes.count', el)
        comments_likes = jmespath.search('comments.count', el)
        ph_date = jmespath.search('date', el)
        max_resolution_id = get_max_resolution_id()

        df_temp.loc[0, 'user_id'] = user_id
        df_temp.loc[0, 'link'] = f'https://vk.com/id{user_id}'
        df_temp.loc[0, 'url'] = urls[max_resolution_id]
        df_temp.loc[0, 'user_likes'] = user_likes
        df_temp.loc[0, 'comments_likes'] = comments_likes
        df_temp.loc[0, 'rating'] = int(user_likes) + int(comments_likes)
        df_temp.loc[0, 'ph_date'] = ph_date
        df_temp.loc[0, 'ph_type'] = ph_types[max_resolution_id]

        df_result = df_result.append(df_temp, ignore_index=True)

    # df_result['user_likes'] = df_result['user_likes'].astype('int')
    # df_result['ph_date'] = df_result['ph_date'].astype('int')

    try:
        df_result['user_id'] = df_result['user_id'].astype('int')
    except Exception as e:
        print(e)

    df_result = get_top_photos(df_result)

    sql_save_res = df_result[['user_id', 'link', 'url']].to_sql('search_results', con=connection, index=False,
                                                                if_exists='append')

    # print('Photos for download:')
    # print(df_result)

    result = df_result[['user_id', 'link', 'url']].to_dict('records')

    return result


def users_get(user_id=None) -> dict:
    if user_id is None:
        user_id = input('Введите VK user_id или screen_name: ')

    def need_more_data():
        nonlocal was_need_more_data
        if not was_need_more_data:
            print('Необходима дополнительная информация!')
            was_need_more_data = True

    def get_city_id(city):
        method_name = '/database.getCities'
        params = {
            'access_token': TOKEN,
            'v': '5.126',
            'q': city
        }
        r = requests.get(HOST + method_name, params=params)
        r.raise_for_status()
        response = r.json()
        city_id = response.get('items')[0].get('id')
        return city_id

    def resolve_screen_name(screen_name):
        method_name = '/utils.resolveScreenName'
        params = {
            'access_token': TOKEN,
            'v': '5.126',
            'screen_name': screen_name
        }
        r = requests.get(HOST + method_name, params=params)
        r.raise_for_status()
        response = r.json()
        if response.get('response').get('type') == 'user':
            user_id = response.get('response').get('object_id')
        else:
            user_id = None
        return user_id, screen_name

    if not str(user_id).isdigit():
        user_id, screen_name = resolve_screen_name(user_id)
        if user_id is None:
            raise Exception(f'can not get user_id via screen_name - {screen_name}')

    now = datetime.datetime.now()
    now_year = now.year
    was_need_more_data = False
    ask_error = False
    result = {}
    method_name = '/users.get'
    params = {
        'access_token': TOKEN,
        'v': '5.126',
        'user_ids': user_id,
        'fields': 'bdate,sex,city,status,relation'
    }

    r = requests.get(HOST + method_name, params=params)
    r.raise_for_status()
    response = r.json()

    if response.get('error'):
        error_code = response['error']['error_code']
        error_msg = response['error']['error_msg']
        raise Exception('API error', error_code, error_msg)

    else:
        result['byear'] = response['response'][0].get('bdate')
        result['sex'] = response['response'][0].get('sex')
        result['city_id'] = response['response'][0].get('city').get('id')
        result['status'] = response['response'][0].get('relation')
        result['user_id'] = user_id

    for i in range(3):
        try:
            my_temp = result['byear'].split('.')[2]
        except (IndexError, AttributeError):
            need_more_data()
            result['byear'] = int(input('Введите год вашего рождения: '))
            if now_year - result['byear'] < 0:
                print('Вы ввели неверный год')
                ask_error = True
            else:
                result['byear'] = '0.0.' + str(result['byear'])

        if result['sex'] is None or result['sex'] == '':
            need_more_data()
            result['sex'] = int(input('Выберете пол: 1 — женщина; 2 — мужчина; 0 — любой'))
            if result['sex'] not in [0, 1, 2]:
                print('Вы ввели неверный пол')
                result['sex'] = None
                ask_error = True

        if result['city_id'] is None or result['city_id'] == '':
            need_more_data()
            city = int(input('Введите город'))
            result['city_id'] = get_city_id(city)

        if result['status'] is None or result['status'] == '':
            need_more_data()
            result['status'] = int(input('''
Выберете варинт статуса:
1 — не женат (не замужем)
2 — встречается
3 — помолвлен(-а)
4 — женат (замужем)
5 — всё сложно
6 — в активном поиске
7 — влюблен(-а)
8 — в гражданском браке
: '''))
            if result['status'] not in [1, 2, 3, 4, 5, 6, 7, 8]:
                print('Вы ввели неверный статус')
                result['status'] = None
                ask_error = True

        if not ask_error:
            break
        elif i != 2:
            ask_error = False
        else:
            raise Exception('can not get right input')

    return result
