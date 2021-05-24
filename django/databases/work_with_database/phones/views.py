from django.shortcuts import render
from phones.management.commands import import_phones
from django.http import HttpResponse
from phones.models import Phone
from django.urls import reverse
from urllib.parse import urlencode


def show_catalog(request):
    template = 'catalog.html'
    order_by = request.GET.get('order_by', None)

    if order_by in ['name', 'release_date', 'lte_exists', 'slug']:
        phones = Phone.objects.all().order_by(order_by)
    elif order_by == 'price_up':
        phones = Phone.objects.all().order_by('price')
    elif order_by == 'price_down':
        phones = Phone.objects.all().order_by('-' + 'price')
    else:
        phones = Phone.objects.all()

    sort_links = {
        'name': f"{reverse('phone_catalog')}?{urlencode({'order_by': 'name'})}",
        'price_up': f"{reverse('phone_catalog')}?{urlencode({'order_by': 'price_up'})}",
        'price_down': f"{reverse('phone_catalog')}?{urlencode({'order_by': 'price_down'})}",
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

    slugs = Phone.objects.values_list('slug', flat=True)

    if slug in slugs:
        phone = Phone.objects.filter(slug=slug)[0]
    else:
        return show_catalog(request)
    context = {'data': phone}
    return render(request, template, context)


def import_phones_view(request):
    phones = import_phones.Command().handle()
    return HttpResponse('Импорт завершен')
