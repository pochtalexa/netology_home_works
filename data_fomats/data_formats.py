import json
import jmespath
import pandas as pd
import xml.etree.ElementTree as ET
from pprint import pprint


# -------------------------------------------------------------------------------------------------------

def read_json(file_name):
    with open(file_name, encoding='utf-8') as f:
        data = json.load(f)
    return data


def get_news_json(data_json):
    result = []
    data = jmespath.search('rss.channel.items[*].description', data_json)
    for el in data:
        result += el.split()
    return result


def get_top_words(data_list, top=10):

    def filter_len(word):
        if len(word) > 6:
            return True
        else:
            return False

    def to_lower(word):
        return word.lower()

    def check_top(df_data, top):
        top = top - 1
        qnty = 0
        index = 0
        for i in df_data.index:
            if i < top:
                continue
            if qnty <= df_data.loc[i, 'count']:
                qnty = df_data.loc[i, 'count']
                index = i
            elif qnty > df_data.loc[i, 'count']:
                break
        return index + 1

    df_data = pd.DataFrame(data=data_list, columns=['word'])
    df_data['word'] = df_data['word'].apply(to_lower)
    df_data = df_data[df_data['word'].apply(filter_len)]
    df_data = (df_data.groupby(by=['word'], as_index=False).size().reset_index().sort_values(by=[0], ascending=False).
               reset_index(drop=True).rename(columns={0: 'count'}))
    top_head = check_top(df_data, top)
    return df_data.head(top_head)


def get_news_xml(file_name):
    result = []
    parser = ET.XMLParser(encoding='utf-8')
    tree = ET.parse(file_name, parser)
    root = tree.getroot()
    descriptions_xml = root.findall('channel/item/description')
    for el in descriptions_xml:
        result += el.text.split()
    return result


# -------------------------------------------------------------------------------------------------------

file_json = read_json('newsafr.json')
news_list = get_news_json(file_json)
df_top_words = get_top_words(news_list, 10)
print('data from JSON:')
print(df_top_words)
print('-'*100)
print()

news_list = get_news_xml('newsafr.xml')
df_top_words = get_top_words(news_list, 10)
print('data from XML:')
print(df_top_words)
print('-'*100)
