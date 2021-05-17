from django.shortcuts import render
import pandas as pd
import json


def inflation_view(request):
    template_name = 'inflation.html'

    # чтение csv-файла и заполнение контекста
    df = pd.read_csv('inflation_russia.csv', delimiter=";")
    df = df.fillna('-')

    context = {'columns': df.columns,
               'col_numbers': list(range(1, len(df.columns))),
               'index': df.index,
               # 'data': df.values.tolist()
               'data': df.to_dict('records')
    }

    return render(request, template_name, context)