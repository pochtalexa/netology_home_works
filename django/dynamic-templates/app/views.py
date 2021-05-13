from django.shortcuts import render
import pandas as pd
import json


def inflation_view(request):
    template_name = 'inflation.html'

    # чтение csv-файла и заполнение контекста
    df = pd.read_csv('inflation_russia.csv', delimiter=";")
    df = df.fillna('-')

    context = {'columns': df.columns,
               'index': df.index,
               'data': df.values.tolist()
    }

    return render(request, template_name, context)