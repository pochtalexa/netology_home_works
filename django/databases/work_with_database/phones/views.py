from django.shortcuts import render
from phones.management.commands import import_phones
from django.http import HttpResponse
from phones.models import Phone
from django.urls import reverse
from urllib.parse import urlencode


def show_catalog(request):
    template = 'catalog.html'
    order_by = request.GET.get('order_by', None)
    show_catalog.counter += 1

    if order_by in ['name', 'release_date', 'lte_exists', 'slug']:
        phones = Phone.objects.all().order_by(order_by)
    elif order_by == 'price':
        if show_catalog.counter % 2:
            phones = Phone.objects.all().order_by(order_by)
        else:
            phones = Phone.objects.all().order_by('-' + order_by)
    else:
        phones = Phone.objects.all()

    sort_links = {
        'name': f"{reverse('phone_catalog')}?{urlencode({'order_by': 'name'})}",
        'price': f"{reverse('phone_catalog')}?{urlencode({'order_by': 'price'})}",
        'release_date': f"{reverse('phone_catalog')}?{urlencode({'order_by': 'release_date'})}",
        'lte_exists': f"{reverse('phone_catalog')}?{urlencode({'order_by': 'lte_exists'})}",
        'slug': f"{reverse('phone_catalog')}?{urlencode({'order_by': 'slug'})}"
    }

    context = {
        'data': phones,
        'sort_links': sort_links,
        'base_link': reverse('phone_catalog')
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.filter(slug=slug)[0]
    context = {'data': phone}
    return render(request, template, context)


def import_phones_view(request):
    phones = import_phones.Command().handle()
    return HttpResponse('Импорт завершен')


show_catalog.counter = 0
