import django_filters
from django.contrib.auth.models import User

from inventory.models import Product, OutputMovement, InputMovement


class ProductsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains', label='Nome do produto')
    material = django_filters.CharFilter(lookup_expr='icontains', label='Material')
    location = django_filters.CharFilter(lookup_expr='icontains', label='Localização')
    brand = django_filters.CharFilter(lookup_expr='icontains', label='Marca')
    reference = django_filters.CharFilter(lookup_expr='icontains', label='Referência')

    class Meta:
        model = Product
        fields = ['name', 'reference','material','location','brand' ]




class OutputMovementFilter(django_filters.FilterSet):
    date = django_filters.DateRangeFilter(label='Data')

    class Meta:
        model = OutputMovement
        fields = ['date','user']

    def __init__(self, *args, **kwargs):
        super(OutputMovementFilter, self).__init__(*args, **kwargs)
        self.filters['user'].queryset = User.objects.filter().all()


class InputMovementFilter(django_filters.FilterSet):
    date = django_filters.DateRangeFilter(label='Data')

    class Meta:
        model = InputMovement
        fields = ['date','user']

    def __init__(self, *args, **kwargs):
        super(InputMovementFilter, self).__init__(*args, **kwargs)
        self.filters['user'].queryset = User.objects.filter().all()