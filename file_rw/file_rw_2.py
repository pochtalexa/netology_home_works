import os
import re
from pprint import pprint


def filter_fl(fl):
    result = []
    for el in fl:
        if re.search(r'^\d\.txt$', el):
            result.append(el)
    return result


def read_files(fl):
    result = {}
    for file in fl:
        with open(file, encoding='utf-8') as f:
            content = f.readlines()
            # result[file] = {'content': content, 'len': len(content)}
            result[file] = content
    result = sorted(result.items(), key=lambda x: len(x[1]))
    return result


def write_file(content):
    with open('result.txt', 'wt', encoding='utf-8') as f:
        counter = 0
        for file_name, cont in content:
            if counter == 0:
                f.write(file_name+'\n')
            else:
                f.write('\n' + file_name + '\n')
            f.write(str(len(cont))+'\n')
            for el in cont:
                f.write(el)
            counter += 1
    return True

# ----------------------------------------------------------------------------------------------------------------

fl = os.listdir()
fl = filter_fl(fl)  # берем файлы c именем вида r'^\d\.txt$'

content = read_files(fl)

write_file(content)