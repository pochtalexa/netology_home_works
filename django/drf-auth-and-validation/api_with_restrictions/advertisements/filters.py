from django_filters import rest_framework as filters
from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    user = filters.CharFilter(field_name="creator__username", lookup_expr='iexact')
    created = filters.DateFromToRangeFilter(field_name="created_at")
    updated = filters.DateFromToRangeFilter(field_name="updated_at")

    class Meta:
        model = Advertisement
        fields = ('user', 'created', 'updated', 'status')
