import django_filters

from inventory.models import Product


class ProductsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Nome do produto')
    reference = django_filters.CharFilter(lookup_expr='icontains', label='Referência')

    class Meta:
        model = Product
        fields = ['name', 'reference', ]
