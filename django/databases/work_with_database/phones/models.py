from django.db import models


class Phone(models.Model):
    # id = models.IntegerField(primary_key=True)
    name = models.TextField()
    price = models.FloatField()
    image = models.ImageField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField()

    def __str__(self):
        return (f'name={self.name}\nprice={self.price}\nimage={self.image}\n'
                f'release_date={self.release_date}\nlte_exists={self.lte_exists}\nslug={self.slug}')
