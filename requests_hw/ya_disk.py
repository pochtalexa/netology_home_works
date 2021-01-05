import requests
from urllib.request import pathname2url
from pprint import pprint

PATH_TO_FILE = './oslyabyajp.jpg'
HOST = 'https://cloud-api.yandex.net:443/'
with open('ya_disk_token.txt') as f:
    TOKEN = f.readline().strip().strip('\n')

# --------------------------------------------------------------------------------------------------

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def upload(self, file_path: str):
        """Метод загруджает файл file_path на яндекс диск"""

        header = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

        # создаем папку
        r = requests.put(HOST + 'v1/disk/resources',
                         headers=header,
                         params={
                             'path': pathname2url('/Downloads'),
                             'overwrite': True
                         })
        # result = r.json()
        # print('create dir', result)

        # получаем ссылку
        r = requests.get(HOST + 'v1/disk/resources/upload',
                         headers=header,
                         params={
                             'path': pathname2url('/Downloads/test.jpg'),
                             'overwrite': True
                         })
        result = r.json()
        href = result['href']
        # print('get url for upload', result)

        # отправляем файл
        with open(file_path, 'rb') as f:
            r = requests.put(href, data=f)
            result_status_code = r.status_code
            result_reason = r.reason
            # print('result', result_status_code, result_reason)

        return result_status_code, result_reason

# --------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    uploader = YaUploader(TOKEN)
    upload_result = uploader.upload(PATH_TO_FILE)
    print(upload_result)
