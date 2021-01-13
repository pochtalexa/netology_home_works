import requests
import time
import jmespath
import pandas as pd
import os
import json
from urllib.request import pathname2url
from pprint import pprint

# отображать все колонки
pd.set_option('display.max_columns', 30)
pd.set_option("max_colwidth", 50)

VK_HOST = 'https://api.vk.com/method'
with open('vk_token.txt') as f:
    VK_TOKEN = f.readline().strip().strip('\n')
TEST_ID = '552934290'  # begemot_korovin

YA_HOST = 'https://cloud-api.yandex.net:443/'
with open('ya_disk_token.txt') as f:
    YA_TOKEN = f.readline().strip().strip('\n')

PATH_TO_FILES = 'photos_download'


# -------------------------------------------------------------------------------------------------

def get_user_info(user_id):
    method_name = '/users.get'
    params = {
        'user_id': user_id,
        'access_token': VK_TOKEN,
        'v': '5.126'
    }
    r = requests.get(VK_HOST + method_name, params=params)
    result = r.json()
    return result['response'][0]


def get_user_photos(user_id, token=VK_TOKEN, count=5):
    method_name = '/photos.get'
    params = {
        'owner_id': user_id,
        'album_id': 'profile',
        'extended': 1,
        'photo_sizes': 1,
        'count': count,
        'access_token': token,
        'v': '5.126'
    }
    r = requests.get(VK_HOST + method_name, params=params)
    result = r.json()
    return result['response']


def get_photos_for_download(user_photos):
    df_result = pd.DataFrame()

    def get_max_resolution_id():
        max_res = 0
        max_res_id = None
        for i, el in enumerate(heights):
            if el > max_res:
                max_res = el
                max_res_id = i
        return max_res_id

    for el in user_photos['items']:
        df_temp = pd.DataFrame()
        heights = jmespath.search('sizes[*].height', el)
        widths = jmespath.search('sizes[*].width', el)
        ph_types = jmespath.search('sizes[*].type', el)
        urls = jmespath.search('sizes[*].url', el)
        user_likes = jmespath.search('likes.count', el)
        ph_date = jmespath.search('date', el)
        max_resolution_id = get_max_resolution_id()

        df_temp.loc[0, 'url'] = urls[max_resolution_id]
        df_temp.loc[0, 'user_likes'] = user_likes
        df_temp.loc[0, 'ph_date'] = ph_date
        df_temp.loc[0, 'ph_type'] = ph_types[max_resolution_id]

        df_result = df_result.append(df_temp, ignore_index=True)

    df_result['user_likes'] = df_result['user_likes'].astype('int')
    df_result['ph_date'] = df_result['ph_date'].astype('int')

    print('Photos for download:')
    print(df_result)
    return df_result


def save_photos_to_hdd(df_user_photos):
    # Создаем директорию для скачивания, если ее нет
    try:
        os.mkdir(PATH_TO_FILES)
    except Exception:
        print(f'Dir "{PATH_TO_FILES}" already exists')

    user_likes_list = list(df_user_photos['user_likes'])
    for ind in df_user_photos.index:
        url = df_user_photos.loc[ind, 'url']
        user_likes = df_user_photos.loc[ind, 'user_likes']
        ph_date = df_user_photos.loc[ind, 'ph_date']

        if user_likes_list.count(user_likes) > 1:
            file_name = f'{user_likes}_{ph_date}.jpg'
        else:
            file_name = f'{user_likes}.jpg'

        df_user_photos.loc[ind, 'file_name'] = file_name

        with open(os.path.join(PATH_TO_FILES, file_name), 'wb') as f:
            r = requests.get(url)
            r.raise_for_status()
            data = r.content
            f.write(data)

    return True


def ya_disk_upload(df_user_photos):
    header = {
        'Content-Type': 'application/json',
        'Authorization': f'OAuth {YA_TOKEN}'
    }

    # создаем папку
    r = requests.put(YA_HOST + 'v1/disk/resources',
                     headers=header,
                     params={
                         'path': pathname2url('/VK_backup'),
                         'overwrite': True
                     })
    # result = r.json()
    # print('create dir', result)

    ya_upload_result = []
    for ind in df_user_photos.index:
        file_name = df_user_photos.loc[ind, 'file_name']
        size = df_user_photos.loc[ind, 'ph_type']

        # получаем ссылку
        r = requests.get(YA_HOST + 'v1/disk/resources/upload',
                         headers=header,
                         params={
                             'path': pathname2url(f'/VK_backup/{file_name}'),
                             'overwrite': True
                         })

        r.raise_for_status()
        result = r.json()
        href = result['href']
        # print('get url for upload', result)

        # отправляем файл
        with open(os.path.join(PATH_TO_FILES, file_name), 'rb') as f:
            r = requests.put(href, data=f)
            r.raise_for_status()
            # result_status_code = r.status_code
            # result_reason = r.reason
            # print('result', result_status_code, result_reason)
            local_result = {
                'file_name': file_name,
                'size': size
            }
            ya_upload_result.append(local_result)
            pprint(f'{ind + 1} from {len(df_user_photos)} - {local_result}')

    with open('result_log.json', 'wt', encoding='utf8') as f:
        json.dump(ya_upload_result, f, indent=4)

    return ya_upload_result


def get_input_params():
    vk_user_id = input('Введите ID пользователя VK: ')
    if vk_user_id == '':
        vk_user_id = TEST_ID

    ya_disk_token = input('Введите Token Ya Disk: ')
    if ya_disk_token == '':
        ya_disk_token = YA_TOKEN

    return vk_user_id, ya_disk_token


# -------------------------------------------------------------------------------------------------

input_params = get_input_params()
user_photos = get_user_photos(input_params[0])
df_user_photos = get_photos_for_download(user_photos)
save_photos_to_hdd(df_user_photos)
ya_disk_upload_log = ya_disk_upload(df_user_photos)
