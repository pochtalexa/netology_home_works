import json


class Countries:

    def __init__(self, read_file_path, write_file_path):
        self.read_file_path = read_file_path
        self.write_file_path = write_file_path
        self.data = self.read_file()
        self.init_file()
        self.ind = -1
        self.link = ''
        self.country = ''

    def __iter__(self):
        return self

    def __next__(self):
        self.ind += 1

        try:
            self.country = self.data[self.ind]['name']['common'].replace(' ', '_')
            self.link = f"https://en.wikipedia.org/wiki/{self.country}"
            self.add_data_to_file()
            return True
        except IndexError:
            raise StopIteration

    def read_file(self):
        with open(self.read_file_path) as f:
            self.data = json.load(f)
        return self.data

    def init_file(self):
        with open(self.write_file_path, 'w', encoding='utf8') as f:
            json.dump({}, f)

    def add_data_to_file(self):
        with open(self.write_file_path, 'r', encoding='utf8') as f:
            current_file = json.load(f)
            current_file[self.country] = self.link
        with open(self.write_file_path, 'w', encoding='utf8') as f:
            json.dump(current_file, f, indent=4)


def main():
    read_file_path = 'countries.json'
    write_file_path = 'results.json'
    countries = Countries(read_file_path, write_file_path)

    for el in countries:
        print(countries.country, countries.link)


if __name__ == '__main__':
    main()
