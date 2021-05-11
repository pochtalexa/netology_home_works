from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404
from .settings import BUS_STATION_CSV
import pandas as pd
import math
import json
from urllib.parse import urlencode



def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    df = pd.read_csv(BUS_STATION_CSV, encoding='cp1251', delimiter=',')
    df = df[['Name', 'Street', 'District']]

    page = request.GET.get('page', 1)

    try:
        page = int(page)
    except Exception as e:
        page = 1

    if page <= 1:
        current_page = 1
        prev_page_url = None
        next_page_url = f"{reverse('bus_stations')}?{urlencode({'page': page + 1})}"
    elif page >= math.ceil(len(df) / 10):
        page = math.ceil(len(df) / 10)
        current_page = page
        prev_page_url = f"{reverse('bus_stations')}?{urlencode({'page': page - 1})}"
        next_page_url = None
    else:
        current_page = page
        prev_page_url = f"{reverse('bus_stations')}?{urlencode({'page': page - 1})}"
        next_page_url = f"{reverse('bus_stations')}?{urlencode({'page': page + 1})}"

    df_result = df[10 * (page - 1):10 * page].reset_index(drop=True)

    result_json = df_result.to_json(orient="records")
    result_json = json.loads(result_json)

    '''
    [{'Name': 'название', 'Street': 'улица', 'District': 'район'},
                         {'Name': 'другое название', 'Street': 'другая улица', 'District': 'другой район'}]
    '''

    context = {
        'bus_stations': result_json,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    }

    return render(request, 'index.html', context=context)
