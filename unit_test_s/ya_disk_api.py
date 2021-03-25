import requests
import json
from urllib.request import pathname2url

# -------------------------------------------------------------------------------------------------

YA_HOST = 'https://cloud-api.yandex.net:443/'

with open('ya_disk_token.txt') as f:
    data = json.load(f)
    YA_TOKEN = data['ya_token']


# -------------------------------------------------------------------------------------------------

def ya_disk_create_folder(folder_name):
    header = {
        'Content-Type': 'application/json',
        'Authorization': f'OAuth {YA_TOKEN}'
    }

    # создаем папку
    r = requests.put(YA_HOST + 'v1/disk/resources',
                     headers=header,
                     params={
                         'path': pathname2url(f'/{folder_name}'),
                         'overwrite': True
                     })
    r_code = r.status_code

    try:
        result = r.json()
    except Exception as e:
        result = None

    print('create dir', result)
    return r_code, result


def ya_disk_delete_folder(folder_name):
    header = {
        'Content-Type': 'application/json',
        'Authorization': f'OAuth {YA_TOKEN}'
    }

    r = requests.delete(YA_HOST + 'v1/disk/resources',
                        headers=header,
                        params={
                            'path': pathname2url(f'/{folder_name}')
                        })
    r_code = r.status_code

    try:
        result = r.json()
    except Exception as e:
        result = None

    print('delete dir', result)
    return r_code, result


# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    print(ya_disk_create_folder('test_folder'))
    print(ya_disk_delete_folder('test_folder'))
    print('done')
