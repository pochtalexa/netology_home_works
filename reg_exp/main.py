import pandas as pd
import csv
import re
from pprint import pprint

# -------------------------------------------------------------------------------------------------
# отображать все колонки
pd.set_option('display.max_columns', 30)
pd.set_option("max_colwidth", 50)


# -------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------
def read_from_csv(file_name):
    with open(file_name, encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def normalize_contacts_list(contacts_list):
    temp_list = []
    header_list = contacts_list[0]
    header_len = len(contacts_list[0])

    for i, el in enumerate(contacts_list):
        if i == 0:
            continue

        if len(el) == header_len:
            temp_list.append(el)
        elif len(el) > header_len:
            temp_list.append(el[0:6])
        else:
            raise Exception(el, 'need more data in row')

    return header_list, temp_list


def normalize_names(row):
    lastname, firstname, surname, organization, position, phone, email = row

    if firstname == surname == '':
        try:
            fio = lastname.split(' ')
            lastname = fio[0]
            firstname = fio[1]
            surname = fio[2]
        except Exception as e:
            pass
    elif firstname != '' and surname == '':
        try:
            fio = firstname.split(' ')
            firstname = fio[0]
            surname = fio[1]
        except Exception as e:
            pass

    return [lastname, firstname, surname, organization, position, phone, email]


def normalize_phone(phone):
    """
    привести все телефоны в формат +7(999)999-99-99.
    Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999;
    """

    pattern_1 = re.compile(r"[-+()\s]+")
    pattern_2 = re.compile(r"^(7|8)(\d{3})(\d{3})(\d{2})(\d{2})\D*(\d{0,4})$")

    phone = pattern_1.sub('', phone)

    if pattern_2.search(phone)[6]:
        result = pattern_2.sub(r"+7(\2)\3-\4-\5 доб.\6", phone)
    else:
        result = pattern_2.sub(r"+7(\2)\3-\4-\5", phone)

    return result


def not_empty(cell_list):
    for el in cell_list:
        if el != '' and el != None:
            return el
    return ''


# -------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    contacts_list = read_from_csv('phonebook_raw.csv')
    header_list, contacts_list = normalize_contacts_list(contacts_list)
    df_contacts = pd.DataFrame(data=contacts_list, columns=header_list)

    df_contacts = df_contacts.apply(normalize_names, axis=1, result_type='broadcast')
    df_contacts = df_contacts.groupby(['lastname', 'firstname']).agg({'surname': not_empty,
                                                                      'organization': not_empty,
                                                                      'position': not_empty,
                                                                      'phone': not_empty,
                                                                      'email': not_empty
                                                                      }).reset_index()
    df_contacts['phone'] = df_contacts['phone'].apply(normalize_phone)

    print(df_contacts)

    df_contacts.to_csv('phonebook_result.csv', sep=';', index_label='id')
