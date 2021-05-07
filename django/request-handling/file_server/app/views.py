from django.shortcuts import render
from app.settings import FILES_PATH
import os
import datetime


def file_list(request, date=None):
    template_name = 'index.html'

    files_list = os.listdir(FILES_PATH)
    files_stat = os.stat(FILES_PATH)

    files = []
    for file_name in files_list:
        files_stat = os.stat(os.path.join(FILES_PATH, file_name))
        file = {'name': file_name,
                'ctime': datetime.datetime.fromtimestamp(files_stat.st_ctime, tz=datetime.timezone.utc),
                'mtime': datetime.datetime.fromtimestamp(files_stat.st_mtime, tz=datetime.timezone.utc)
        }

        if date is None:
            files.append(file)
        elif file['ctime'].date() == date.date():
            files.append(file)

    context = {'files': files}

    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:

    # context = {
    #     'files': [
    #         {'name': 'file_name_1.txt',
    #          'ctime': datetime.datetime(2018, 1, 1),
    #          'mtime': datetime.datetime(2018, 1, 2)}
    #     ],
    #     'date': datetime.date(2018, 1, 1)  # Этот параметр необязательный
    # }

    return render(request, template_name, context)


def file_content(request, name):
    # Реализуйте алгоритм подготавливающий контекстные данные для шаблона по примеру:

    context = {'file_name': name}

    with open(os.path.join(FILES_PATH, name), 'rt') as f:
        file_content = f.read()

    context = {'file_content': file_content}

    # ={'file_name': 'file_name_1.txt', 'file_content': 'File content!'}

    return render(request, 'file_content.html', context)
