import hashlib


def make_md5_hash(path_to_file):
    with open(path_to_file, 'rb') as f:
        while True:
            data = f.readline()
            if data == b'':
                break
            yield data, hashlib.md5(data).hexdigest()


def main():
    path_to_file = 'countries.json'
    for d, h in make_md5_hash(path_to_file):
        print(d, '==', h)


if __name__ == '__main__':
    main()


