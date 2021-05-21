import csv
import pandas as pd

from django.core.management.base import BaseCommand
from phones.models import Phone
from django.template.defaultfilters import slugify


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    # def handle(self, *args, **options):
    #     with open('phones.csv', 'r') as csvfile:
    #
    #         phone_reader = csv.reader(csvfile, delimiter=';')
    #         # пропускаем заголовок
    #         next(phone_reader)
    #
    #         for line in phone_reader:
    #             # TODO: Добавьте сохранение модели
    #             pass

    def handle(self):

        df = pd.read_csv('phones.csv', delimiter=';', index_col=False)

        for ind in df.index:
            name = df.loc[ind, 'name']
            price = df.loc[ind, 'price']
            image = df.loc[ind, 'image']
            release_date = df.loc[ind, 'release_date']
            lte_exists = df.loc[ind, 'lte_exists']
            slug = slugify(name)

            p = Phone(name=name, price=price, image=image, release_date=release_date, lte_exists=lte_exists, slug=slug)

            p.save()


